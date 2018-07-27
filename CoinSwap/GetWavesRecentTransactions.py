import requests
import sys

def get_waves_recent_transactions_json(str_wallet_address):
    try:
        res = requests.get('https://nodes.wavesnodes.com/transactions/address/' + str_wallet_address + '/limit/100')
        res.raise_for_status()
        return res.text
    except:
        return r'{ "status":"error", "message":"invalid address" }'




if __name__ == '__main__':
    ret = get_waves_recent_transactions_json("abc")
    print(ret);
    print("-------------------------")
    ret = get_waves_recent_transactions_json("3PFCT4q6K56zC8YGa8vBaXgvkfFvJnRdFF8")
    print(ret);
    print("-------------------------")    
    ret = get_waves_recent_transactions_json("0x494Da578D0470A2E43B8668826De87e6BC74bECf")
    print(ret);
    print("-------------------------")        