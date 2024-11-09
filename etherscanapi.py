import requests
from dotenv import load_dotenv
import os

load_dotenv()

api = 'https://api.etherscan.io/api'
API_KEY = os.getenv("ETHERSCAN_API_KEY")
PARAMS = {
    "module": "account",
    "action": "tokentx",
    "contractaddress": "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2",
    "page": 1,
    "offset": 100,
    "startblock": 0,
    "endblock": 27025780,
    "sort": "asc",
    "apikey": API_KEY
}

resp = requests.get(api, params=PARAMS)
print(resp.text)
