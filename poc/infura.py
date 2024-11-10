from web3 import Web3

# Connect to an Ethereum node (replace with your node URL)
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/d0c3df955cd946c1ad28b5eaca3160d9'))

# Get the latest block number
latest_block = w3.eth.get_block("latest")["number"]
print("Latest Block Number:", latest_block)
