import requests
import json

# Constants
WALLET_ADDRESS = "0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5"
API_KEY = "9UZW78WJ8KWUJAGYCM9I4X7NM66Q74S7MZ"
BASE_URL = "https://api.etherscan.io/api"

# ETH Transactions
eth_payload = {
    "module": "account",
    "action": "txlist",
    "address": WALLET_ADDRESS,
    "startblock": 0,
    "endblock": 99999999,
    "sort": "asc",
    "apikey": API_KEY
}
eth_response = requests.get(BASE_URL, params=eth_payload)
eth_data = eth_response.json()

if eth_data['status'] != "1":
    raise Exception("Error fetching ETH transaction data")

eth_transactions = eth_data['result']
eth_sent_transactions = [tx for tx in eth_transactions if tx['from'].lower() == WALLET_ADDRESS.lower()]
eth_received_transactions = [tx for tx in eth_transactions if tx['to'].lower() == WALLET_ADDRESS.lower()]
eth_created_contracts = [tx for tx in eth_transactions if not tx['to']]

eth_sent_values = [int(tx['value']) / 10**18 for tx in eth_sent_transactions]
eth_received_values = [int(tx['value']) / 10**18 for tx in eth_received_transactions]

eth_sent_times = [int(tx['timeStamp']) for tx in eth_sent_transactions]
eth_received_times = [int(tx['timeStamp']) for tx in eth_received_transactions]
eth_times = [int(tx['timeStamp']) for tx in eth_transactions]

# ERC20 Transactions
erc20_payload = {
    "module": "account",
    "action": "tokentx",
    "address": WALLET_ADDRESS,
    "startblock": 0,
    "endblock": 99999999,
    "sort": "asc",
    "apikey": API_KEY
}
erc20_response = requests.get(BASE_URL, params=erc20_payload)
erc20_data = erc20_response.json()

if erc20_data['status'] != "1":
    raise Exception("Error fetching ERC20 transaction data")

erc20_transactions = erc20_data['result']
erc20_sent_transactions = [tx for tx in erc20_transactions if tx['from'].lower() == WALLET_ADDRESS.lower()]
erc20_received_transactions = [tx for tx in erc20_transactions if tx['to'].lower() == WALLET_ADDRESS.lower()]

erc20_sent_values = [int(tx['value']) / 10**int(tx['tokenDecimal']) for tx in erc20_sent_transactions]
erc20_received_values = [int(tx['value']) / 10**int(tx['tokenDecimal']) for tx in erc20_received_transactions]

# Calculate metrics for ETH
eth_sent_avg_time = sum(eth_sent_times[i+1] - eth_sent_times[i] for i in range(len(eth_sent_times)-1)) / len(eth_sent_times) if len(eth_sent_times) > 1 else 0
eth_received_avg_time = sum(eth_received_times[i+1] - eth_received_times[i] for i in range(len(eth_received_times)-1)) / len(eth_received_times) if len(eth_received_times) > 1 else 0
eth_overall_avg_time = sum(eth_times[i+1] - eth_times[i] for i in range(len(eth_times)-1)) / len(eth_times) if len(eth_times) > 1 else 0

# Calculate times for ERC20 transactions
erc20_sent_times = [int(tx['timeStamp']) for tx in erc20_sent_transactions]
erc20_received_times = [int(tx['timeStamp']) for tx in erc20_received_transactions]
erc20_times = [int(tx['timeStamp']) for tx in erc20_transactions]

# Calculate average times for ERC20 transactions
erc20_sent_avg_time = sum(erc20_sent_times[i+1] - erc20_sent_times[i] for i in range(len(erc20_sent_times)-1)) / (len(erc20_sent_times) - 1) if len(erc20_sent_times) > 1 else 0
erc20_received_avg_time = sum(erc20_received_times[i+1] - erc20_received_times[i] for i in range(len(erc20_received_times)-1)) / (len(erc20_received_times) - 1) if len(erc20_received_times) > 1 else 0
erc20_overall_avg_time = sum(erc20_times[i+1] - erc20_times[i] for i in range(len(erc20_times)-1)) / (len(erc20_times) - 1) if len(erc20_times) > 1 else 0


# Calculate metrics for ERC20
erc20_sent_avg_time = sum(erc20_sent_times[i+1] - erc20_sent_times[i] for i in range(len(erc20_sent_times)-1)) / len(erc20_sent_times) if len(erc20_sent_times) > 1 else 0
erc20_received_avg_time = sum(erc20_received_times[i+1] - erc20_received_times[i] for i in range(len(erc20_received_times)-1)) / len(erc20_received_times) if len(erc20_received_times) > 1 else 0
erc20_overall_avg_time = sum(erc20_times[i+1] - erc20_times[i] for i in range(len(erc20_times)-1)) / len(erc20_times) if len(erc20_times) > 1 else 0

# Combine ETH and ERC20 metrics
combined_metrics = {
    # ETH Metrics
    'ETH Avg min between sent tnx': eth_sent_avg_time / 60,  # Convert to minutes
    'ETH Avg min between received tnx': eth_received_avg_time / 60,  # Convert to minutes
    'ETH Time Diff between first and last (Mins)': eth_overall_avg_time / 60,  # Convert to minutes
    'ETH Sent tnx': len(eth_sent_transactions),
    'ETH Received Tnx': len(eth_received_transactions),
    'ETH Number of Created Contracts': len(eth_created_contracts),
    'ETH Unique Received From Addresses': len(set(tx['from'] for tx in eth_received_transactions)),
    'ETH Unique Sent To Addresses': len(set(tx['to'] for tx in eth_sent_transactions)),
    'ETH min value received': min(eth_received_values) if eth_received_values else 0,
    'ETH max value received': max(eth_received_values) if eth_received_values else 0,
    'ETH avg val received': sum(eth_received_values) / len(eth_received_values) if eth_received_values else 0,
    'ETH min val sent': min(eth_sent_values) if eth_sent_values else 0,
    'ETH max val sent': max(eth_sent_values) if eth_sent_values else 0,
    'ETH avg val sent': sum(eth_sent_values) / len(eth_sent_values) if eth_sent_values else 0,
    'ETH total transactions (including tnx to create contract)': len(eth_transactions),
    'ETH total Ether sent': sum(eth_sent_values),
    'ETH total ether received': sum(eth_received_values),
    # ERC20 Metrics
    'ERC20 Avg min between sent tnx': erc20_sent_avg_time / 60,  # Convert to minutes
    'ERC20 Avg min between received tnx': erc20_received_avg_time / 60,  # Convert to minutes
    'ERC20 Time Diff between first and last (Mins)': erc20_overall_avg_time / 60,  # Convert to minutes
    'ERC20 Sent tnx': len(erc20_sent_transactions),
    'ERC20 Received Tnx': len(erc20_received_transactions),
    'ERC20 Unique Sent To Addresses': len(set(tx['to'] for tx in erc20_sent_transactions)),
    'ERC20 Unique Received From Addresses': len(set(tx['from'] for tx in erc20_received_transactions)),
    'ERC20 min val received': min(erc20_received_values) if erc20_received_values else 0,
    'ERC20 max val received': max(erc20_received_values) if erc20_received_values else 0,
    'ERC20 avg val received': sum(erc20_received_values) / len(erc20_received_values) if erc20_received_values else 0,
    'ERC20 min val sent': min(erc20_sent_values) if erc20_sent_values else 0,
    'ERC20 max val sent': max(erc20_sent_values) if erc20_sent_values else 0,
    'ERC20 avg val sent': sum(erc20_sent_values) / len(erc20_sent_values) if erc20_sent_values else 0,
    'ERC20 total tnxs': len(erc20_transactions),
    'ERC20 total Ether received': sum(erc20_received_values),
    'ERC20 total ether sent': sum(erc20_sent_values),
}

json_output = json.dumps(combined_metrics, indent=4)
print(json_output)
