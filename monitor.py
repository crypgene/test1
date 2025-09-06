from web3 import Web3
import time

# Configuration Alchemy
ALCHEMY_WSS = "wss://eth-mainnet.g.alchemy.com/v2/U1BgaYMB7eHyex4a-efAH"  # Remplacez par votre clé WebSocket
w3 = Web3(Web3.WebsocketProvider(ALCHEMY_WSS))

# ABI minimal pour vérifier name et symbol
ERC20_ABI = [
    {"constant": True, "inputs": [], "name": "name", "outputs": [{"name": "", "type": "string"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"name": "", "type": "string"}], "type": "function"}
]

def check_new_token(contract_address):
    try:
        contract = w3.eth.contract(address=contract_address, abi=ERC20_ABI)
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        if name == "Arcade Bot" or symbol == "ARCADE":
            print(f"Nouveau token détecté !\nAdresse : {contract_address}\nNom : {name}\nSymbole : {symbol}\nVérifiez sur Etherscan : https://etherscan.io/address/{contract_address}")
        else:
            print(f"Contrat vérifié : {contract_address}, Nom : {name}, Symbole : {symbol} (non correspondant)")
    except Exception as e:
        print(f"Erreur lors de la vérification du contrat {contract_address} : {e}")

def monitor_transactions():
    print("Démarrage du monitoring...")
    while True:
        try:
            # Récupérer les transactions du dernier bloc
            block = w3.eth.get_block('latest', full_transactions=True)
            print(f"Vérification du bloc {block['number']}...")
            for tx in block['transactions']:
                # Vérifier si c’est une création de contrat
                if tx.get('to') is None:
                    receipt = w3.eth.get_transaction_receipt(tx['hash'])
                    if receipt.get('contractAddress'):
                        contract_address = receipt['contractAddress']
                        print(f"Nouveau contrat détecté : {contract_address}")
                        check_new_token(contract_address)
            time.sleep(10)  # Attendre 10s avant le prochain bloc
        except Exception as e:
            print(f"Erreur lors de la récupération du bloc : {e}")
            time.sleep(10)

if __name__ == "__main__":
    if w3.is_connected():
        print("Connecté à Ethereum via Alchemy")
        monitor_transactions()
    else:
        print("Connexion à Alchemy échouée")