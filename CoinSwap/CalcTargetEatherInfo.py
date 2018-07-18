import json
import sys
import os.path

def IsExistEtherWalletDirectory(path):
    if os.path.isdir(path):
        return True
    else:
        return False


def GetTransitionFiles(path):
    if IsExistEtherWalletDirectory(path):
        return os.listdir(path)
    else:
        return []


def GetEtherWillSendAmount(ether_address):
    dir = r"postdata/" + ether_address + "/"
    file_list = GetTransitionFiles(dir)
    eth_amount = 0
    for f in file_list:
        try:
            p = open(dir+f, 'r')
            json_data = json.load(p)
            p.close()
            eth_amount = eth_amount + json_data["eth_amount"]
        except:
            print(sys.exc_info())
            pass

    return {"eth_amount": eth_amount}


# テスト
if __name__ == '__main__':
    ret = GetEtherWillSendAmount(r"0x494Da578D0470A2E43B8668826De87e6BC74bECf")
    print(ret)


