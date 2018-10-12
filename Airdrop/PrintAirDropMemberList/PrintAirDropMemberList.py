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
import traceback


def CalkOneAirDropData(path):
        try:
	        with open(path, "r") as fr:
	            airdropinfo = json.load(fr)
	            print(airdropinfo["user_id"] + "\t" + airdropinfo["eth_address"])

        except Exception as e:
            print("エラー" + path)
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))

def CalkAllEtherData():
    dirlist = os.listdir("./AirdropMemberInfo")
    # print(dirlist)
    for d in dirlist:
        CalkOneAirDropData("./AirdropMemberInfo/" + d)


CalkAllEtherData()