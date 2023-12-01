## [Frontend](https://dirtymoneydetector.streamlit.app)
🔗 Streamlit → [Source Code](./web)

---

## [API](https://dirtyapi.replit.app)
### Path: `/api/<wallet_address>`
### Output:
```json
{
  "Address": "string",
  "Avg min between received tnx": "float",
  "Avg min between sent tnx": "float",
  "AvgValSent": "float",
  "AvgValueReceived5Average": "float",
  "AvgValueSentToContract": "int",
  "ERC20AvgTimeBetweenRec_Tnx": "float",
  "ERC20AvgTimeBetweenSent_Tnx": "float",
  "ERC20AvgVal_Rec": "float",
  "ERC20AvgVal_Sent": "float",
  "ERC20MaxVal_Rec": "float",
  "ERC20MaxVal_Sent": "float",
  "ERC20MinVal_Rec": "float",
  "ERC20MinVal_Sent": "float",
  "ERC20MostRecTokenType": "string",
  "ERC20MostSentTokenType": "string",
  "ERC20TotalEtherSentContract": "float",
  "ERC20TotalEther_Received": "float",
  "ERC20TotalEther_Sent": "float",
  "ERC20UniqRecContractAddr": "int",
  "ERC20UniqRecTokenName": "int",
  "ERC20UniqRec_Addr": "int",
  "ERC20UniqSentTokenName": "int",
  "ERC20UniqSent_Addr": "int",
  "MaxValSent": "float",
  "MaxValueReceived": "float",
  "MaxValueSentToContract": "float",
  "MinValSent": "float",
  "MinValueReceived": "float",
  "MinValueSentToContract": "float",
  "NumberofCreated_Contracts": "int",
  "Received_tnx": "int",
  "Sent_tnx": "int",
  "Time Diff between first and_last (Mins)": "float",
  "TotalERC20Tnxs": "int",
  "TotalEtherBalance": "float",
  "TotalEtherReceived": "float",
  "TotalEtherSent": "float",
  "TotalEtherSent_Contracts": "float",
  "TotalTransactions": "int",
  "UniqueReceivedFrom_Addresses": "int",
  "UniqueSentTo_Addresses20": "int"
}
```
---
## ML Model
🔗 [Source Code](./ML)

---

## How to Use 

1. Clone the Repository 
```bash 
 git clone https://github.com/sr2echa/dirty-moni-detector.git
```

2. Install all requirments and dependencies
```bash
pip install -r requirments.txt
```
3. Run the application:
```bash
streamlit run website.py
```

---

## Tech Stack 
<figure style="text-align: right;">
  <img src="web/Group 323.png" alt="Tech Stack" style="width:300px;height:300px;">
</figure>

- [x] Streamlit
- [x] Tensorflow
- [x] Github
- [x] replit
- [x] Flask
- [x] Seaborn

 ---

> [!IMPORTANT]
> **Made for RevaHack 23 ❤️** <br>
> <samp> We even won the **1st place** and were the **Title Winners of RevaHack 23**! More about it here 👉 <a href="https://devfolio.co/projects/dmd-dirty-money-detector-54b2">Devfolio</a> </samp>

