import os
import requests
from collections import Counter
from flask import jsonify

# Load API keys from environment variables
ETH_API_KEY = os.getenv("ETH_API_KEY")
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
BNB_API_KEY = os.getenv("BNB_API_KEY")

# API URLs
API_URLS = {
    'eth': "https://api.etherscan.io/api",
    'polygon': "https://api.polygonscan.com/api",
    'bnb': "https://api.bscscan.com/api"
}

# Initialize a session object
session = requests.Session()

def fetch_blockchain_data(chain, wallet_address):
    api_key = os.getenv(f"{chain.upper()}_API_KEY")
    api_url = API_URLS[chain]

    def get_transactions(action):
        payload = {
            "module": "account",
            "action": action,
            "address": wallet_address,
            "startblock": 0,
            "endblock": 99999999,
            "sort": "asc",
            "apikey": api_key
        }
        response = session.get(api_url, params=payload)
        return response.json()['result'] if response.json()['status'] == "1" else []

    def process_transactions(transactions, is_erc20=False):
        sent_transactions = [tx for tx in transactions if tx['from'].lower() == wallet_address.lower()]
        received_transactions = [tx for tx in transactions if tx['to'].lower() == wallet_address.lower()]
        created_contracts = [tx for tx in transactions if not tx['to']]

        def get_value(tx):
            return int(tx['value']) / 10**18 if not is_erc20 else int(tx['value']) / 10**int(tx.get('tokenDecimal', '18'))

        metrics = {
            "Sent_tnx": len(sent_transactions),
            "Received_tnx": len(received_transactions),
            "NumberofCreated_Contracts": len(created_contracts),
            "UniqueReceivedFrom_Addresses": len(set(tx['from'] for tx in received_transactions)),
            "UniqueSentTo_Addresses": len(set(tx['to'] for tx in sent_transactions)),
            "MinValueReceived": min((get_value(tx) for tx in received_transactions), default=0),
            "MaxValueReceived": max((get_value(tx) for tx in received_transactions), default=0),
            "AvgValueReceived": sum(get_value(tx) for tx in received_transactions) / len(received_transactions) if received_transactions else 0,
            "MinValueSent": min((get_value(tx) for tx in sent_transactions), default=0),
            "MaxValueSent": max((get_value(tx) for tx in sent_transactions), default=0),
            "AvgValueSent": sum(get_value(tx) for tx in sent_transactions) / len(sent_transactions) if sent_transactions else 0,
            "TotalTransactions": len(transactions),
            "TotalEtherSent": sum(get_value(tx) for tx in sent_transactions),
            "TotalEtherReceived": sum(get_value(tx) for tx in received_transactions),
            "TotalEtherBalance": sum(get_value(tx) for tx in received_transactions) - sum(get_value(tx) for tx in sent_transactions),
        }

        if is_erc20:
            token_types = Counter(tx['tokenSymbol'] for tx in transactions)
            metrics.update({
                "TotalERC20Tnxs": len(transactions),
                "ERC20UniqSent_Addr": len(set(tx['to'] for tx in sent_transactions)),
                "ERC20UniqRec_Addr": len(set(tx['from'] for tx in received_transactions)),
                "ERC20UniqSentTokenName": len(token_types),
                "ERC20MostSentTokenType": token_types.most_common(1)[0][0] if token_types else None,
            })

        return metrics

    # Get standard transactions
    transactions = get_transactions('txlist')
    metrics = process_transactions(transactions)

    # Get ERC20 token transactions
    erc20_transactions = get_transactions('tokentx')
    erc20_metrics = process_transactions(erc20_transactions, is_erc20=True)

    # Combine both metrics
    combined_metrics = {**metrics, **erc20_metrics}

    return combined_metrics

def eth(wallet_address):
    try:
        return jsonify(fetch_blockchain_data('eth', wallet_address))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def polygon(wallet_address):
    try:
        return jsonify(fetch_blockchain_data('polygon', wallet_address))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def bnb(wallet_address):
    try:
        return jsonify(fetch_blockchain_data('bnb', wallet_address))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
