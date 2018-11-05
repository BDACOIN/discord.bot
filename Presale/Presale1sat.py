import requests
import sys
import re
import json
import builtins

def get_input_jpy(text):

    m1 = re.search("^(.+?)\s*(YEN|JPY)?$", text, re.IGNORECASE)
    try:
        print(m1)
        yen = m1.group(1)
        return float(yen)
    except:
        pass

    m2 = re.search("^(.+?)\s*(ETH)$", text, re.IGNORECASE)
    try:
        print(m2)
        eth = m2.group(1)
        return float(eth) * float(get_eth_jpy())
    except:
        pass

    m3 = re.search("^(.+?)\s*(BTC)$", text, re.IGNORECASE)
    try:
        print(m3)
        btc = m3.group(1)
        return float(btc) * float(get_btc_jpy())
    except:
        pass

    print("糞")


def get_btc_jpy():
    try:
        res = requests.get('https://coincheck.com/api/rate/btc_jpy')
        res.raise_for_status()
        python_obj = json.loads(res.text)
        return float(python_obj["rate"])
    except:
        return 0

def get_eth_jpy():
    try:
        res = requests.get('https://coincheck.com/api/rate/eth_jpy')
        res.raise_for_status()
        python_obj = json.loads(res.text)
        return float(python_obj["rate"])
    except:
        return 0


def get_bda_num(msg):
    btc_jpy = get_btc_jpy()
    input_jpy = get_input_jpy(msg)
    print("結果" + str(input_jpy))
    bda_sat = 0.00000001
    
    return input_jpy / (btc_jpy * bda_sat)

def is_permission_teamhousyu_condition(message):
    ch = str(message.channel)
    if ch in ["プリセール計算君"]:
       return True

    return False

async def say_message(message):
    ret = get_bda_num(message.content)
    
    if ret+10000 >= 100000000:
        ret = ret * 1.3
    elif ret+10000 >= 50000000:
        ret = ret * 1.2
    elif ret+10000 >= 10000000:
        ret = ret * 1.12
    elif ret+10000 >= 5000000:
        ret = ret * 1.1

    if ret+3000 < 1000000:
        await client.send_message(message.channel, "0.01 BTC に満たないようです。")
    else:
        await client.send_message(message.channel, str(int(round(ret, -1))) + " 枚 の BDA")


# テスト
if __name__ == '__main__':
    # btc_jpy = get_btc_jpy()
    # input_jpy = get_input_jpy("86500")
    
    ret = get_bda_num("1.5ETH")
    print(ret)
    