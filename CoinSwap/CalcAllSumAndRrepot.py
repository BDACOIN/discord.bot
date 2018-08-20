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

def CalkOneEtherData(dirname):
    # print(dirname)
    msg = dirname.strip()
    if JudgeErrorWalletAddress.is_message_ether_pattern(msg):
        ret = CalcTargetEatherInfo.GetEtherWillSendAmount(msg)
        try:
            adresslist.append(msg)
            amountlist.append(ret["eth_amount"])
            if len(ret["user_id_list"]) > 1:
                # print("複数人から１つのイーサアドレスに送金されたデータです。")
                pass
        except:
            print("エラーデータを発見:" + dirname )

def CalkAllEtherData():
    dirlist = os.listdir("./postdata")
    # print(dirlist)
    for d in dirlist:
        CalkOneEtherData(d)


CalkAllEtherData()

#print(adresslist)
#print(amountlist)


collected_count = 13


report = ""
pre_ix = 0
while(True):
    ix = pre_ix + collected_count
    report += str(adresslist[pre_ix:ix]) + "\n"
    report += str(amountlist[pre_ix:ix]) + "\n"
    report += "\n"
    pre_ix = ix
    if ix > len(adresslist):
        break


report = report.replace("'", '"')

path = './report.txt'
f = open(path, "w")
f.write(report)
f.close()


print("総計額:" + str(sum(amountlist)))

