import requests
import sys
import re

def get_waves_recent_transactions_json(p):
    try:
        res = requests.get('https://etherscan.io/token/generic-tokenholders2?a=0xf6caa4bebd8fab8489bc4708344d9634315c4340&s=0&p=1')
        res.raise_for_status()
        return res.text
    except:
        return None




if __name__ == '__main__':
    ret = get_waves_recent_transactions_json(1)
    # print(ret)
    # ret_list = re.findall("<tr><td>\d+</td><td><span><a href='/token/0xf6caa4bebd8fab8489bc4708344d9634315c4340?a=(0x.+?)' target='_parent'>0x.+?</a></span></td><td>(\d+)</td><td>\d+%</td></tr>", ret)
    ret_list = re.findall("<tr><td>\d+</td><td><span><a href='/token/0xf6caa4bebd8fab8489bc4708344d9634315c4340\?a=(0x.+?)' target='_parent'>0x.+?</a></span></td><td>(\d+)</td><td>\d+%</td></tr>", ret)
    print(ret_list)
