import os
import requests
import json
from collections import Counter
from datetime import datetime

from dotenv import load_dotenv
load_dotenv(".env")
# os.environ['variable']

import flask
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


ETH_API_KEY = os.environ["ETH_API_KEY"]
POLYGON_API_KEY = os.environ["POLYGON_API_KEY"]

ETHSCAN_URL = "https://api.etherscan.io/api"
POLYGON_URL = "https://api.polygonscan.com/api"


#WALLET_ADDRESS =  "0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5"#"0x677e813fee748f9467de2f00a5ad9d1d8cf365bb" #"0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5"




@app.route('/')
def index():
    return jsonify({"message": "Welcome to DMD"})

@app.route('/api/<WALLET_ADDRESS>')
def api(WALLET_ADDRESS):
    eth_payload = {
        "module": "account",
        "action": "txlist",
        "address": WALLET_ADDRESS,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": ETH_API_KEY
    }
    eth_response = requests.get(ETHSCAN_URL, params=eth_payload)
    eth_data = eth_response.json()

    # Fetch ERC20 Transactions
    erc20_payload = {
        "module": "account",
        "action": "tokentx",
        "address": WALLET_ADDRESS,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": ETH_API_KEY
    }
    erc20_response = requests.get(ETHSCAN_URL, params=erc20_payload)
    erc20_data = erc20_response.json()

    # Initialize data structures
    eth_transactions = eth_data['result'] if eth_data['status'] == "1" else []
    erc20_transactions = erc20_data['result'] if erc20_data['status'] == "1" else []

    # Process ETH Transactions
    eth_sent_transactions = [tx for tx in eth_transactions if tx['from'].lower() == WALLET_ADDRESS.lower()]
    eth_received_transactions = [tx for tx in eth_transactions if tx['to'].lower() == WALLET_ADDRESS.lower()]
    created_contracts = [tx for tx in eth_transactions if not tx['to']]

    eth_sent_times = [int(tx['timeStamp']) for tx in eth_sent_transactions]
    eth_received_times = [int(tx['timeStamp']) for tx in eth_received_transactions]
    eth_times = [int(tx['timeStamp']) for tx in eth_transactions]

    # Process ERC20 Transactions
    erc20_sent_transactions = [tx for tx in erc20_transactions if tx['from'].lower() == WALLET_ADDRESS.lower()]
    erc20_received_transactions = [tx for tx in erc20_transactions if tx['to'].lower() == WALLET_ADDRESS.lower()]

    erc20_sent_times = [int(tx['timeStamp']) for tx in erc20_sent_transactions]
    erc20_received_times = [int(tx['timeStamp']) for tx in erc20_received_transactions]

    # ERC20 Token Types
    sent_token_types = Counter(tx['tokenSymbol'] for tx in erc20_sent_transactions)
    received_token_types = Counter(tx['tokenSymbol'] for tx in erc20_received_transactions)

    combined_metrics = {
        "Address": WALLET_ADDRESS,
        "Avg min between sent tnx": sum(eth_sent_times[i+1] - eth_sent_times[i] for i in range(len(eth_sent_times)-1)) / len(eth_sent_times) if len(eth_sent_times) > 1 else 0,
        "Avg min between received tnx": sum(eth_received_times[i+1] - eth_received_times[i] for i in range(len(eth_received_times)-1)) / len(eth_received_times) if len(eth_received_times) > 1 else 0,
        "Time Diff between first and_last (Mins)": (max(eth_times) - min(eth_times)) / 60 if eth_times else 0,
        "Sent_tnx": len(eth_sent_transactions),
        "Received_tnx": len(eth_received_transactions),
        "NumberofCreated_Contracts": len(created_contracts),
        "UniqueReceivedFrom_Addresses": len(set(tx['from'] for tx in eth_received_transactions)),
        "UniqueSentTo_Addresses20": len(set(tx['to'] for tx in eth_sent_transactions)),
        "MinValueReceived": min((int(tx['value']) for tx in eth_received_transactions), default=0) / 10**18,
        "MaxValueReceived": max((int(tx['value']) for tx in eth_received_transactions), default=0) / 10**18,
        "AvgValueReceived5Average": sum(int(tx['value']) for tx in eth_received_transactions) / len(eth_received_transactions) / 10**18 if eth_received_transactions else 0,
        "MinValSent": min((int(tx['value']) for tx in eth_sent_transactions), default=0) / 10**18,
        "MaxValSent": max((int(tx['value']) for tx in eth_sent_transactions), default=0) / 10**18,
        "AvgValSent": sum(int(tx['value']) for tx in eth_sent_transactions) / len(eth_sent_transactions) / 10**18 if eth_sent_transactions else 0,
        "MinValueSentToContract": min((int(tx['value']) for tx in created_contracts), default=0) / 10**18,
        "MaxValueSentToContract": max((int(tx['value']) for tx in created_contracts), default=0) / 10**18,
        "AvgValueSentToContract": sum(int(tx['value']) for tx in created_contracts) / len(created_contracts) / 10**18 if created_contracts else 0,
        "TotalTransactions": len(eth_transactions),
        "TotalEtherSent": sum(int(tx['value']) for tx in eth_sent_transactions) / 10**18,
        "TotalEtherReceived": sum(int(tx['value']) for tx in eth_received_transactions) / 10**18,
        "TotalEtherSent_Contracts": sum(int(tx['value']) for tx in created_contracts) / 10**18,
        "TotalEtherBalance": (sum(int(tx['value']) for tx in eth_received_transactions) - sum(int(tx['value']) for tx in eth_sent_transactions)) / 10**18,
        "TotalERC20Tnxs": len(erc20_transactions),
        "ERC20TotalEther_Received": sum(int(tx['value']) for tx in erc20_received_transactions) / 10**18,
        "ERC20TotalEther_Sent": sum(int(tx['value']) for tx in erc20_sent_transactions) / 10**18,
        "ERC20TotalEtherSentContract": sum(int(tx['value']) for tx in erc20_sent_transactions if 'contractAddress' in tx) / 10**18,
        "ERC20UniqSent_Addr": len(set(tx['to'] for tx in erc20_sent_transactions)),
        "ERC20UniqRec_Addr": len(set(tx['from'] for tx in erc20_received_transactions)),
        "ERC20UniqRecContractAddr": len(set(tx['contractAddress'] for tx in erc20_received_transactions)),
        "ERC20AvgTimeBetweenSent_Tnx": sum(erc20_sent_times[i+1] - erc20_sent_times[i] for i in range(len(erc20_sent_times)-1)) / len(erc20_sent_times) if len(erc20_sent_times) > 1 else 0,
        "ERC20AvgTimeBetweenRec_Tnx": sum(erc20_received_times[i+1] - erc20_received_times[i] for i in range(len(erc20_received_times)-1)) / len(erc20_received_times) if len(erc20_received_times) > 1 else 0,
        "ERC20MinVal_Rec": min((int(tx['value']) for tx in erc20_received_transactions), default=0) / 10**18,
        "ERC20MaxVal_Rec": max((int(tx['value']) for tx in erc20_received_transactions), default=0) / 10**18,
        "ERC20AvgVal_Rec": sum(int(tx['value']) for tx in erc20_received_transactions) / len(erc20_received_transactions) / 10**18 if erc20_received_transactions else 0,
        "ERC20MinVal_Sent": min((int(tx['value']) for tx in erc20_sent_transactions), default=0) / 10**18,
        "ERC20MaxVal_Sent": max((int(tx['value']) for tx in erc20_sent_transactions), default=0) / 10**18,
        "ERC20AvgVal_Sent": sum(int(tx['value']) for tx in erc20_sent_transactions) / len(erc20_sent_transactions) / 10**18 if erc20_sent_transactions else 0,
        "ERC20UniqSentTokenName": len(sent_token_types),
        "ERC20UniqRecTokenName": len(received_token_types),
        "ERC20MostSentTokenType": sent_token_types.most_common(1)[0][0] if sent_token_types else None,
        "ERC20MostRecTokenType": received_token_types.most_common(1)[0][0] if received_token_types else None,
    }
    
    return jsonify(combined_metrics)




if __name__ == '__main__':
    app.run(debug=True, port=5000)
