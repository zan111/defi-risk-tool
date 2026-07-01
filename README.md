📌 DeFi Risk Analytics Tool

A Python-based analytics platform for evaluating decentralized finance (DeFi) lending risk, including collateral health, liquidation thresholds, and stress testing scenarios using real-time blockchain data.

🎯 Project Overview

This project simulates a risk analytics engine for DeFi lending protocols.
It calculates key financial risk metrics such as:

Loan-to-Value (LTV)
Health Factor
Liquidation thresholds
Stress scenarios under price volatility

The goal is to demonstrate how traditional risk analytics can be applied to blockchain-based financial systems.

⚙️ Features
Real-time DeFi data ingestion via The Graph API
Portfolio-level risk calculations
Collateral and debt position analysis
Stress testing under market volatility scenarios
Interactive dashboard for risk visualization
🧠 Key Metrics
Health Factor → measures position safety against liquidation
Loan-to-Value (LTV) → exposure vs collateral ratio
Liquidation Threshold → risk trigger level
Stress Test Scenarios → simulated price drops and risk impact
🏗️ Tech Stack
Python
Pandas
NumPy
Plotly
Dash / Streamlit (depending on your version)
The Graph API
📊 Example Use Case

A user deposits crypto assets as collateral and borrows stablecoins.

This tool:

tracks collateral value
monitors risk exposure in real time
simulates liquidation risk under market downturns
visualizes portfolio health dynamically
💡 Business Relevance

This project demonstrates core skills required in fintech / crypto analytics roles:

Risk modelling
Data pipeline design
Financial metrics computation
Blockchain data extraction
Decision-support analytics systems

Demo: [link to live app if deployed]

Instructions:
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `python app.py`
