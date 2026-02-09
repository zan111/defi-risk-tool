import requests
import pandas as pd
import streamlit as st

"""
# --> deprecated
def get_coin_list():
    headers = {"accept": "application/json"}
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 250, "page": 1}
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1"
    response = requests.get(url, headers=headers, params=params)
    
    try:
        data = response.json()
    except Exception:
        st.error("CoinGecko API returned invalid JSON. Cannot continue.")
        st.stop()
    
    data = pd.DataFrame(data)
    
    if "symbol" not in data.columns or data.empty:
        st.error("CoinGecko API did not return 'symbol' data. Cannot continue.")
        st.stop()
    
    # merge reserves coins with price coin from coingecko
    data["symbol"] = data["symbol"].str.upper()
    data.rename(columns={"current_price": "Price"}, inplace=True)
    df_reserves = get_reserves()
    merged_df = pd.merge(df_reserves, data, on="symbol", how="inner")
    
    if merged_df.empty:
        st.error("No matching coins between reserves and CoinGecko. Cannot continue.")
        st.stop()
    
    merged_df[["Price", "market_cap", "total_volume", "totalLiquidity", "totalBorrows"]] = merged_df[["Price", "market_cap", "total_volume", "totalLiquidity", "totalBorrows"]].astype(float)
    return merged_df
"""

def get_reserves():
    api = "c1de085f872244b8443afbff0ade7aa0"
    subgraph_id = "JCNWRypm7FYwV8fx5HhzZPSFaMxgkPuw4TnR3Gpi81zk"
    url = f"https://gateway.thegraph.com/api/{api}/subgraphs/id/{subgraph_id}"
    
    query = """
    {
        markets(first: 1000) {
            inputToken {
                symbol
                lastPriceUSD
            }
            totalDepositBalanceUSD
            totalBorrowBalanceUSD
            liquidationThreshold
        }
    }
    """
    
    response = requests.post(url, json={"query": query})
    data = response.json()
    
    # ✅ The Graph returns data under 'data' → 'markets'
    markets = data.get("data", {}).get("markets", [])
    result = {"reserves": []}
    
    for market in markets:
        token = market["inputToken"]
        result["reserves"].append({
            "symbol": token["symbol"],
            "totalLiquidity": market["totalDepositBalanceUSD"],
            "totalBorrows": market["totalBorrowBalanceUSD"],
            "liquidationThreshold": market["liquidationThreshold"],
            "Price": token["lastPriceUSD"]
        })
    
    df = pd.DataFrame(result["reserves"])
    
    if "symbol" not in df.columns or df.empty:
        print("symbol not found")
    
    df["symbol"] = df["symbol"].str.upper()
    df[["Price", "totalLiquidity", "totalBorrows", "liquidationThreshold"]] = df[["Price", "totalLiquidity", "totalBorrows", "liquidationThreshold"]].astype(float)
    
    # removes assets which don't have liquidationThreshold and price
    df = df[(df["liquidationThreshold"] > 0) & (df["Price"] > 0)]
    
    return df