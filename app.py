
# ------------------------- app.py -------------------------
from dash import Dash, html, dash_table, dcc, Input, Output, State, ALL
import dash 
import pandas as pd
from calculations import general_calc, calculate_hf, calculate_ltv, hf_ratio_description, stress_test_calculation_multiple
from fetch_data import get_reserves
from visualization import hf_bar_figure, ltv_bar_figure, price_change_figure



# Fetch default chain data at app start
print("🔄 Fetching coin data from The Graph...")
df_coins = get_reserves()
print(f"✅ Loaded {len(df_coins)} coins")

if len(df_coins) == 0:
    print("❌ WARNING: No coins loaded! Check API connection.")
    coin_list = []
else:
    coin_list = df_coins["symbol"].tolist()
    print(f"📋 Coins available: {coin_list[:5]}... (showing first 5)")


# Initialize app
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server


def evaluate_row_risk(row, stressed_df):
    """Returns True if this row contributes to risk after stress."""
    symbol = row.get("Coin", "")
    if not symbol:
        return False

    # Get price change
    before = stressed_df.loc[stressed_df["symbol"] == symbol, "Price_before"].mean()
    after = stressed_df.loc[stressed_df["symbol"] == symbol, "Price_after"].mean()

    # Risk if price dropped more than -10%
    if before > 0 and (after / before) < 0.90:
        return True

    return False

print(f"🔍 DEBUG: coin_list has {len(coin_list)} items")
print(f"First 10: {coin_list[:10] if coin_list else 'EMPTY!'}")


# Layout
app.layout = html.Div(
    style={
        "backgroundColor": "#f5f6fa",
        "padding": "30px",
        "fontFamily": "Arial, sans-serif"
    },
    children=[
        html.H1(
            "DeFi Risk Tool",
            style={"textAlign": "center", "marginBottom": "30px"}
        ),
html.Div(
    style={
        "marginBottom": "25px",
        "backgroundColor": "white",
        "padding": "25px",
        "borderRadius": "12px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"
    },
    children=[
        html.H2("About the Tool", style={"marginTop": "0"}),
        html.P(
            "This DeFi Risk Tool helps you analyze your lending and borrowing positions on decentralized finance platforms. "
            "You can enter your supplied and borrowed assets, calculate your Health Factor (HF), Loan-to-Value (LTV), and run stress tests to see how market volatility impacts your portfolio."
            "\nData is fetched from Aave V3 on the Ethereum chain only via The Graph subgraph."
        ),
    ]
),



# ------------------- Deposits Section -------------------
html.Div(
    style={
        "backgroundColor": "white",
        "padding": "25px",
        "borderRadius": "12px",
        "marginBottom": "25px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"
    },
    children=[
        html.H3("Deposits", style={"marginTop": "0"}),
        dash_table.DataTable(
            id="table-deposits",
            columns=[
                {"name": "Coin", "id": "Coin", "presentation": "dropdown"},
                {"name": "Amount", "id": "Amount", "type": "numeric"},
                {"name": "Risk", "id": "Risk", "type": "numeric"}
            ],
            style_cell_conditional=[
                {"if": {"column_id": "Risk"}, "display": "none"},
            ],
            data=[{"Coin": "", "Amount": "", "Risk": 0}],
            editable=True,
            row_deletable=True,
            dropdown={},  # Will be populated by callback
            style_table={
                "overflowX": "auto",
            },
            style_cell={
                "textAlign": "left",
                "padding": "10px",
                "fontSize": "14px",
                "minWidth": "120px",
                "width": "150px",
                "maxWidth": "200px",
            },
            style_header={
                "fontWeight": "bold",
                "backgroundColor": "#f8f9fa"
            },
            style_data_conditional=[
                {
                    "if": {"filter_query": "{Risk} = 1"},
                    "backgroundColor": "#ffcccc",
                    "color": "black",
                }
            ],
            css=[{
                'selector': '.Select-menu-outer',
                'rule': 'max-height: 300px !important;'
            }]        
            ),
        html.Button(
            "Add Row",
            id="add-deposit",
            n_clicks=0,
            style={
                "marginTop": "10px",
                "padding": "8px 16px",
                "borderRadius": "8px",
                "backgroundColor": "#2e4ecc",
                "color": "white",
                "border": "none",
                "cursor": "pointer"
            }
        ),
    ]
),


# ------------------- Borrows Section -------------------
html.Div(
    style={
        "backgroundColor": "white",
        "padding": "25px",
        "borderRadius": "12px",
        "marginBottom": "25px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"
    },
    children=[
        html.H3("Borrows", style={"marginTop": "0"}),
        dash_table.DataTable(
            id="table-borrows",
            columns=[
                {"name": "Coin", "id": "Coin", "presentation": "dropdown"},
                {"name": "Amount", "id": "Amount", "type": "numeric"},
                {"name": "Risk", "id": "Risk", "type": "numeric"}
            ],
            style_cell_conditional=[
                {"if": {"column_id": "Risk"}, "display": "none"},
            ],
            data=[{"Coin": "", "Amount": "", "Risk": 0}],
            editable=True,
            row_deletable=True,
            dropdown={},  # Will be populated by callback
            style_table={
                "overflowX": "auto",
            },
            style_cell={
                "textAlign": "left",
                "padding": "10px",
                "fontSize": "14px",
                "minWidth": "120px",
                "width": "150px",
                "maxWidth": "200px",
            },
            style_header={
                "fontWeight": "bold",
                "backgroundColor": "#f8f9fa"
            },
            style_data_conditional=[
                {
                    "if": {"filter_query": "{Risk} = 1"},
                    "backgroundColor": "#ffd6cc",
                    "color": "black",
                }
            ],
            css=[{
                'selector': '.Select-menu-outer',
                'rule': 'max-height: 300px !important;'
            }]  
                ),
        html.Button(
            "Add Row",
            id="add-borrow",
            n_clicks=0,
            style={
                "marginTop": "10px",
                "padding": "8px 16px",
                "borderRadius": "8px",
                "backgroundColor": "#2ecc71",
                "color": "white",
                "border": "none",
                "cursor": "pointer"
            }
        ),
    ]
),

#-----------------Reset--------------------------
html.Button(
    "Reset All",
    id="btn-reset",
    n_clicks=0,
    style={
        "padding": "10px 20px",
        "borderRadius": "8px",
        "backgroundColor": "#c0392b",
        "color": "white",
        "border": "none",
        "cursor": "pointer",
        "fontSize": "16px",
        "marginBottom": "20px"
    }
),

        # ------------------- Calculate Button + Results -------------------
# NEW - Keep this section, but remove the duplicate below
        html.Div(
            style={"marginBottom": "20px"},
            children=[
                html.H4("📊 Key Metrics", style={"marginTop": "0"}),
                html.P(
                    "• Health Factor (HF): Indicates position safety. HF > 1 = healthy, HF < 1 = liquidation risk.",
                    style={"marginBottom": "8px", "color": "#555"}
                ),
                html.P(
                    "• Loan-to-Value (LTV): Borrowed amount vs collateral value. Lower LTV = safer position.",
                    style={"marginBottom": "8px", "color": "#555"}
                ),
            ]
        ),
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "25px",
                "borderRadius": "12px",
                "marginBottom": "25px",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"
            },
            children=[
                html.Button(
                    "Calculate",
                    id="btn-calc",
                    n_clicks=0,
                    style={
                        "padding": "10px 20px",
                        "borderRadius": "8px",
                        "backgroundColor": "#8e44ad",
                        "color": "white",
                        "border": "none",
                        "cursor": "pointer",
                        "fontSize": "16px",
                        "transition": "0.2s",
                        ":hover": {
                            "boxShadow": "0 0 8px rgba(0,0,0,0.2)"
                        }

                    }
                ),
                html.Br(), html.Br(),
                html.Div(id="calc-output", style={"fontSize": "16px"})
            ]
        ),
        

        # ------------------- Stress Test -------------------
        html.P(
            "Stress Test allows you to simulate sudden price changes in your supplied or borrowed assets. "
            "It helps you understand how your Health Factor and LTV change during market volatility.",
            style={"marginBottom": "15px", "color": "#555"}
        ),

        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "25px",
                "borderRadius": "12px",
                "marginBottom": "25px",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"
            },
            children=[
                html.H3("Stress Test"),

                html.Label("Select borrowed coins"),
                dcc.Dropdown(
                    id="stress-borrow-select",
                    multi=True,
                    style={"marginBottom": "15px"}
                ),

                html.Label("Select supplied coins"),
                dcc.Dropdown(
                    id="stress-supply-select",
                    multi=True,
                    style={"marginBottom": "15px"}
                ),

                html.Div(id="stress-sliders-container", style={"marginBottom": "20px"}),

                html.Button(
                    "Run Stress Test",
                    id="run-stress",
                    n_clicks=0,
                    style={
                        "padding": "10px 20px",
                        "borderRadius": "8px",
                        "backgroundColor": "#e67e22",
                        "color": "white",
                        "border": "none",
                        "cursor": "pointer",
                        "fontSize": "16px",
                        ":hover": {
                            "boxShadow": "0 0 8px rgba(0,0,0,0.2)"
                        }
                    }
                ),

                html.Br(), html.Br(),
                html.Div(id="stress-results", style={"fontSize": "16px"}),
                html.Div(
                        id="stress-legend",
                        style={
                            "marginTop": "12px",
                            "backgroundColor": "#fcfcfc",
                            "padding": "12px",
                            "borderRadius": "8px",
                            "border": "1px solid #eee",
                            "color": "#333",
                            "fontSize": "14px"
                        },
                            children=[
                                html.P("HF = Health Factor. If HF < 1 → liquidation risk.", style={"margin":"4px 0"}),
                                html.P("LTV = Loan-to-Value. Higher % = more leveraged.", style={"margin":"4px 0"}),
                                html.P("Rows highlighted indicate assets flagged as risky after the stress test.", style={"margin":"4px 0"})
                            ]
                        )

            ]
        ),

        # ------------------- Stress Charts -------------------
        html.P(
            "These charts show how your Health Factor evolves under different stress scenarios. "
            "They help identify which assets contribute most to your portfolio risk.",
            style={"marginBottom": "15px", "color": "#555"}
        ),

html.Div(
    style={
        "backgroundColor": "white",
        "padding": "25px",
        "borderRadius": "12px",
        "marginBottom": "25px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"
    },
    children=[
        html.H3("Stress Test Visualizations"),
        dcc.Graph(id="hf_bar_chart"),        # HF bar chart
        dcc.Graph(id="ltv_bar_chart"),       # LTV bar chart
        dcc.Graph(id="price_change_chart"),  # Price change per coin chart
    ]
),

        dcc.Store(id="store-portfolio")
    ]
)

# -------------------- Callbacks --------------------


# Add this NEW callback to initialize dropdowns on page load
@app.callback(
    Output("table-deposits", "dropdown"),
    Output("table-borrows", "dropdown"),
    Input("table-deposits", "id"),  # Dummy input to trigger on load
    Input("table-borrows", "id")     # Dummy input to trigger on load
)
def initialize_dropdowns(_, __):
    """Populate dropdowns when page loads"""
    dropdown_config = {
        "Coin": {
            "options": [{"label": c, "value": c} for c in coin_list]
        }
    }
    print(f"🔄 Initializing dropdowns with {len(coin_list)} coins")
    return dropdown_config, dropdown_config

# Add row callbacks
@app.callback(
    Output("table-deposits","data", allow_duplicate=True),
    Output("table-deposits","dropdown", allow_duplicate=True),
    Input("add-deposit","n_clicks"),
    State("table-deposits","data"),
    State("table-deposits","columns"),
    prevent_initial_call=True
)
def add_deposit_row(n, rows, columns):
    if n and rows is not None:
        rows.append({c["id"]: (0 if c["id"] == "Risk" else "") for c in columns})
    
    # Always return the dropdown with fresh data
    dropdown = {
        "Coin": {
            "options": [{"label": c, "value": c} for c in coin_list]
        }
    }
    return rows, dropdown

@app.callback(
    Output("table-borrows","data", allow_duplicate=True),
    Output("table-borrows","dropdown", allow_duplicate=True),
    Input("add-borrow","n_clicks"),
    State("table-borrows","data"),
    State("table-borrows","columns"),
    prevent_initial_call=True
)
def add_borrow_row(n, rows, columns):
    if n and rows is not None:
        rows.append({c["id"]: (0 if c["id"] == "Risk" else "") for c in columns})
    
    # Always return the dropdown with fresh data
    dropdown = {
        "Coin": {
            "options": [{"label": c, "value": c} for c in coin_list]
        }
    }
    return rows, dropdown

@app.callback(
    Output("table-deposits","data"),
    Output("table-borrows","data"),
    Input("btn-reset","n_clicks")
)
def reset_all(n):
    if not n:
        return dash.no_update, dash.no_update
    return [{"Coin": "", "Amount": "", "Risk": 0}], [{"Coin": "", "Amount": "", "Risk": 0}]



# Calculate portfolio
@app.callback(
    Output("calc-output","children"),
    Output("stress-borrow-select","options"),
    Output("stress-supply-select","options"),
    Output("store-portfolio","data", allow_duplicate=True),
    Input("btn-calc","n_clicks"),
    State("table-deposits","data"),
    State("table-borrows","data"),
    prevent_initial_call=True,
)
# NEW:
def calculate_portfolio(n, deposits, borrows):
    if n == 0 or not deposits or not borrows:
        return "Enter deposits and borrows, then click Calculate.", [], [], {}
    
    df_dep = pd.DataFrame(deposits)
    df_dep["Type"] = "Deposit"
    df_bor = pd.DataFrame(borrows)
    df_bor["Type"] = "Borrow"
    
    df_total = pd.concat([df_dep, df_bor], ignore_index=True)
    # Standardize: use 'symbol' consistently
    if "Coin" in df_total.columns:
        df_total.rename(columns={"Coin":"symbol"}, inplace=True)
    
    # Merge with coin data
    df_total = df_total.merge(df_coins, on="symbol", how="left")    
    df_total["Amount"] = pd.to_numeric(df_total["Amount"], errors="coerce").fillna(0)
    df_total["Price"] = pd.to_numeric(df_total["Price"], errors="coerce").fillna(0)
    df_total["liquidationThreshold"] = pd.to_numeric(df_total["liquidationThreshold"], errors="coerce").fillna(0)
    
    df_total = general_calc(df_total)
    if "Risk" not in df_total.columns:
        df_total["Risk"] = 0
    else:
        # Replace empty strings with NA, coerce non-numeric to NaN, fill with 0, then convert to int
        df_total["Risk"] = pd.to_numeric(df_total["Risk"].replace("", pd.NA), errors="coerce").fillna(0).astype(int)

    
    hf = calculate_hf(df_total)
    ltv = calculate_ltv(df_total)
    hf_text = hf_ratio_description(hf)
    
    borrow_options = [{"label":c,"value":c} for c in df_total.loc[df_total["Type"]=="Borrow","symbol"].unique()]
    supply_options = [{"label":c,"value":c} for c in df_total.loc[df_total["Type"]=="Deposit","symbol"].unique()]
    
    return [html.P(hf_text), html.P(f"LTV: {round(ltv,2)}")], borrow_options, supply_options, df_total.to_dict(orient="records")

# Generate sliders dynamically
@app.callback(
    Output("stress-sliders-container","children"),
    Input("stress-borrow-select","value"),
    Input("stress-supply-select","value")
)
def create_sliders(borrowed, supplied):
    sliders = []

    # Sliders for borrowed coins
    for c in borrowed or []:
        sliders.append(html.Div([html.Label(f"Borrowed {c} drop (%)"),
            dcc.Slider(id={"type":"stress-slider","index":f"borrow-{c}"}, min=0, max=100, step=1, value=25,
                    marks={0:"0%",25:"25%",50:"50%",75:"75%",100:"100%"},
                    tooltip={"placement": "bottom", "always_visible": True}),
            html.Br()]))

    # Sliders for supplied coins
    for c in supplied or []:
        sliders.append(html.Div([html.Label(f"Supplied {c} drop (%)"),
            dcc.Slider(id={"type":"stress-slider","index":f"supply-{c}"}, min=0, max=100, step=1, value=25,
                    marks={0:"0%",25:"25%",50:"50%",75:"75%",100:"100%"},
                    tooltip={"placement": "bottom", "always_visible": True}),
            html.Br()]))

    return sliders if sliders else "Select coins to stress."



# Run stress test and update visualizations
# Run stress test and update visualizations
# Run stress test and update visualizations + tables + store
@app.callback(
    Output("stress-results", "children"),
    Output("hf_bar_chart", "figure"),
    Output("ltv_bar_chart", "figure"),
    Output("price_change_chart", "figure"),
    Output("table-deposits", "data", allow_duplicate=True),
    Output("table-borrows", "data", allow_duplicate=True),
    Output("store-portfolio", "data", allow_duplicate=True),
    Input("run-stress", "n_clicks"),
    State({"type": "stress-slider", "index": ALL}, "value"),
    State({"type": "stress-slider", "index": ALL}, "id"),
    State("store-portfolio", "data"),
    prevent_initial_call=True
)

def run_stress_visual(n, values, ids, portfolio_data):
    if n == 0:
        return "", {}, {}, {}, dash.no_update, dash.no_update, dash.no_update
    if not portfolio_data:
        return "No portfolio data stored. Calculate first.", {}, {}, {}, dash.no_update, dash.no_update, dash.no_update

    # Create stress input dictionary
    stress_inputs = {f"{id_['index']}": val for id_, val in zip(ids, values)}

    # DataFrame from stored portfolio
    df = pd.DataFrame(portfolio_data)

    # Run stress test - THIS CREATES stressed_df
    stressed_df, prices = stress_test_calculation_multiple(df, stress_inputs)

    # --- Calculate metrics before & after ---
    hf_before = calculate_hf(df)
    hf_after = calculate_hf(stressed_df)
    ltv_before = calculate_ltv(df)
    ltv_after = calculate_ltv(stressed_df)

    # --- Risk evaluation function ---
    def eval_risk_row(record, prices_map, hf_after_val):
        sym = record.get("symbol", "")
        if not sym:
            return 0
        # Flag as risky if HF < 1
        if hf_after_val is not None and hf_after_val < 1.0:
            return 1
        # Flag as risky if price dropped > 10%
        p = prices_map.get(sym)
        if p and p["old"] > 0 and (p["new"] / p["old"]) < 0.90:
            return 1
        return 0

    # Now stressed_df is available from above
    stressed_records = stressed_df.copy()
    # Ensure Risk column exists and is properly typed
    stressed_records["Risk"] = stressed_records.apply(
        lambda r: eval_risk_row(r, prices, hf_after), axis=1
    )

    # Prepare DataTables with consistent column naming
    table_records = stressed_records.to_dict(orient="records")
    deposits_table = [
        {
            "Coin": rec.get("symbol", ""),
            "Amount": rec.get("Amount", 0),
            "Risk": int(rec.get("Risk", 0))
        }
        for rec in table_records if rec.get("Type") == "Deposit"
    ]
    borrows_table = [
        {
            "Coin": rec.get("symbol", ""),
            "Amount": rec.get("Amount", 0),
            "Risk": int(rec.get("Risk", 0))
        }
        for rec in table_records if rec.get("Type") == "Borrow"
    ]

    # --- Display results ---
    results = [
        html.H4("Stress Test Results"),
        html.P(f"Health Factor (HF) before: {hf_before:.3f}"),
        html.P(f"Health Factor (HF) after: {hf_after:.3f}"),
        html.P(f"Loan-to-Value (LTV) before: {ltv_before:.2f}%"),
        html.P(f"Loan-to-Value (LTV) after: {ltv_after:.2f}%"),
        html.Br(),
        html.P("Price changes: " + ", ".join([f"{k}: {v['old']:.6f} → {v['new']:.6f}" for k, v in prices.items()]))
    ]

    # --- Visuals ---
    hf_bar = hf_bar_figure(hf_before, hf_after)
    ltv_bar = ltv_bar_figure(ltv_before, ltv_after)
    price_chart = price_change_figure(df, stressed_df)

    return results, hf_bar, ltv_bar, price_chart, deposits_table, borrows_table, stressed_records.to_dict(orient="records")
# Run server
if __name__ == "__main__":
    app.run_server(debug=True)




