#coding: utf-8
# ver 2.1
import builtins

import re
import json
import types
import base64
import os
import sys
import datetime
import time
import glob
import JudgeErrorWalletAddress
import CalcTargetEatherInfo

adresslist = []
amountlist = []


def MakeOneEtherData(dirname):
    # print(dirname)
    msg = dirname.strip()
    
    memberinfo = {
        "eth_address": "",
        "waves_address": "",
        "omikuji_ticket_count": 0,
        "roulette_ticket_count": 0,
        "food_ticket_count": 0,
        "drink_ticket_count": 0,
        "kaiwa_experiment": 0,
        "kaiwa_experiment_coef": 1,
        "blog_lv": 0,
        "twitter_lv": 0,
        "facebook_lv": 0,
        "kaiwa_lv": 0,
        "user_id": 0
    }

    paidinfo = {
        "kaiwa_paid_lv": 0,
        "blog_paid_lv": 0,
        "invite_paid_lv": 0,
        "twitter_paid_lv": 0,
        "facebook_paid_lv": 0,
        "kaiwa_paid_amount": 0,
        "blog_paid_amount": 0,
        "twitter_paid_amount": 0,
        "facebook_paid_amount": 0,
        "invite_paid_amount": 0,
        "swap_amount": 0,
        "user_id": 0
    }
    
    if JudgeErrorWalletAddress.is_message_ether_pattern(msg):
        ret = CalcTargetEatherInfo.GetEtherWillSendAmount(msg)
        print(ret)
        try:
            memberinfo["user_id"] = ret["user_id_list"][0]
            memberinfo["eth_address"] = dirname
            memberinfo["omikuji_ticket_count"] = 3
            
            path = 'DataMemberInfo/' + str(memberinfo["user_id"]) + ".json"
            f = open(path, "w")
            json_data = json.dumps(memberinfo, indent=4)
            f.write(json_data)
            f.close()

            if len(ret["user_id_list"]) > 1:
                # print("複数人から１つのイーサアドレスに送金されたデータです。")
                pass

            paidinfo["user_id"] = ret["user_id_list"][0]
            paidinfo["swap_amount"] = ret["eth_amount"]
            path = 'DataMemberPaid/' + str(memberinfo["user_id"]) + ".json"
            f = open(path, "w")
            json_data = json.dumps(paidinfo, indent=4)
            f.write(json_data)
            f.close()

        except:
            print("エラーデータを発見:" + dirname )

def MakeAllEtherData():
    dirlist = os.listdir("./postdata")
    # print(dirlist)
    for d in dirlist:
        MakeOneEtherData(d)


MakeAllEtherData()




