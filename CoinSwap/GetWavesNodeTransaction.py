import requests
import sys
import re

def is_waves_transaction_regex_pattern(string):
    if re.match("^[0-9a-zA-Z]{44}$", string):
        return True
    
    return False

def get_waves_node_transaction_json(str_transaction_address):
    try:
        res = requests.get('https://nodes.wavesnodes.com/transactions/info/' + str_transaction_address)
        res.raise_for_status()
        return res.text
    except:
        return r'{ "status":"error", "details":"Transaction is not in blockchain" }'

