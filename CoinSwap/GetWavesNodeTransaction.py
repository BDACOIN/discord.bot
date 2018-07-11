import requests
import sys

def get_waves_node_transaction_json(str_transaction_address):
    try:
        res = requests.get('https://nodes.wavesnodes.com/transactions/info/' + str_transaction_address)
        res.raise_for_status()
        return res.text
    except:
        return r'{ "status":"error", "details":"Transaction is not in blockchain" }'

