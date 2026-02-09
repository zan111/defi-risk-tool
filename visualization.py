# ------------------------- visualization.py -------------------------
# Plotly-based visualization helpers so they can be embedded in Dash
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# HF bar chart
def hf_bar_figure(hf_before, hf_after):
    df = pd.DataFrame([
        {'Scenario': 'Before', 'Value': hf_before},
        {'Scenario': 'After', 'Value': hf_after}
    ])
    fig = px.bar(df, x='Scenario', y='Value', text='Value',
                 color='Scenario', color_discrete_map={'Before':'#636EFA', 'After':'#EF553B'})
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(title='Health Factor (HF) Before vs After Stress', template='plotly_white')
    return fig

# LTV bar chart
def ltv_bar_figure(ltv_before, ltv_after):
    df = pd.DataFrame([
        {'Scenario': 'Before', 'Value': ltv_before},
        {'Scenario': 'After', 'Value': ltv_after}
    ])
    fig = px.bar(df, x='Scenario', y='Value', text='Value',
                 color='Scenario', color_discrete_map={'Before':'#00CC96', 'After':'#AB63FA'})
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(title='Loan-to-Value (LTV) Before vs After Stress', template='plotly_white', yaxis_title='%')
    return fig

# Price change per coin (percentage)
def price_change_figure(df_before: pd.DataFrame, df_after: pd.DataFrame):
    before = df_before[['symbol','Price']].drop_duplicates().set_index('symbol')
    after = df_after[['symbol','Price']].drop_duplicates().set_index('symbol')
    merged = before.join(after, lsuffix='_before', rsuffix='_after', how='outer').reset_index().fillna(0)
    
    # % change
    merged['Price_change_pct'] = (merged['Price_after'] - merged['Price_before']) / merged['Price_before'] * 100

    fig = go.Figure()
    for _, row in merged.iterrows():
        fig.add_trace(go.Bar(
            name=row['symbol'],
            x=['% Change'],
            y=[row['Price_change_pct']],
            text=f"{row['Price_change_pct']:.2f}%",
            textposition='outside'
        ))

    fig.update_layout(
        barmode='group',
        title='Price Change per Coin After Stress',
        template='plotly_white',
        yaxis_title='Price Change (%)'
    )
    return fig


# ------------------------- END -------------------------
# NOTE: Save each section into separate files (app.py, calculations.py, fetch_data.py, visualization.py) before running.
# To run locally: set environment variables THEGRAPH_API_KEY and THEGRAPH_SUBGRAPH_ID, then `python app.py`.
