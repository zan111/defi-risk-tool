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

App Snips 

1# User loads data for the coins 


<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/d336a6e3-b126-4757-981d-321f7fb2ca46" />

2# Enter his portfolio holdings 


<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/11313f18-8e6a-46b0-9a41-5869920f13fe" />

3# Apply the macro indicators and desired simulations


<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/9c5fde12-1a3a-413f-959f-01cb2266fc38" />

4# Results after running 

<img width="1498" height="896" alt="image" src="https://github.com/user-attachments/assets/e67bb923-ead4-4cf0-b69b-e1f31e7d4916" />


<img width="1525" height="732" alt="image" src="https://github.com/user-attachments/assets/00e95469-d369-4f76-a780-50d355a530f4" />


<img width="1509" height="741" alt="image" src="https://github.com/user-attachments/assets/069ceccb-8772-4bb3-bd95-dc0db272bfbc" />


<img width="1546" height="728" alt="image" src="https://github.com/user-attachments/assets/cb3ecc6f-8ab9-4671-9442-03ad3c89b6d8" />


<img width="1867" height="892" alt="image" src="https://github.com/user-attachments/assets/b5f3f2de-c49e-446c-b93b-013b791c861f" />


<img width="1909" height="898" alt="image" src="https://github.com/user-attachments/assets/08cd8361-a300-4433-8c30-cc8fb129be30" />


<img width="1880" height="886" alt="image" src="https://github.com/user-attachments/assets/f78a1bde-9eb0-4105-9d23-9a20923b69d9" />


<img width="1863" height="816" alt="image" src="https://github.com/user-attachments/assets/9538a3d9-5d38-4a63-93ce-5b3bd4f87290" />


Instructions:
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `python app.py`
