import f

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


ETH_API_KEY = os.getenv("ETH_API_KEY")
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
BNB_API_KEY = os.getenv("BNB_API_KEY")

ETHSCAN_URL = "https://api.etherscan.io/api"
POLYGON_URL = "https://api.polygonscan.com/api"
BNB_URL = "https://api.bscscan.com/api"


#WALLET_ADDRESS =  "0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5"#"0x677e813fee748f9467de2f00a5ad9d1d8cf365bb" #"0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5"




@app.route('/')
def index():
    return jsonify({"message": "Welcome to DMD"})

@app.route('/api/<WALLET_ADDRESS>')
def api(WALLET_ADDRESS):
    return {**f.eth(WALLET_ADDRESS), **f.bnb(WALLET_ADDRESS), **f.polygon(WALLET_ADDRESS)}




if __name__ == '__main__':
    app.run(debug=True, port=5000)
