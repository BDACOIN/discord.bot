#coding: utf-8
# ver 2.1

import builtins
import re
import random
import requests
import json
import types
import base64
import os
import sys, datetime, time
import discord
import traceback
import unicodedata
import difflib

import copy
import asyncio




def ending_scroll_sanka():




    dirlist = os.listdir("./DataHalloweenPokerInfo")
    
    all_result_hash = {}
    # print(dirlist)
    for d in dirlist:
        path = "./DataHalloweenPokerInfo/" + d
        
        try:
            with open(path, "r") as fr:
                pokerinfo = json.load(fr)

            amount = 0
            id = pokerinfo["id"]
            
            for v in pokerinfo["amount"].values():
                amount = amount + v
                
            all_result_hash[id] = amount
                
        except Exception as e2:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e2.__traceback__))
            print("例外:calc_of_all_poker")
            
    sorted_list = sorted(all_result_hash.items(), key=lambda x: x[1], reverse=True )

    modified_sorted_list = []
    for sl in sorted_list:
        if True:
            modified_sorted_list.append(sl)


    index_list_ix = 1
    

    result_list = []
    result_add = []
    
    for s in modified_sorted_list:

        member_id_str = s[0]
        with open("../DiaTan/DataMemberInfo/" + member_id_str + ".json", "r") as mfr:
            memberinfo = json.load(mfr)

            result_list.append(memberinfo["eth_address"])
            result_add.append(str(s[1]))

        try:
            if index_list_ix >= 15 or s is modified_sorted_list[-1]:

                print("[ \"" + "\",\"".join(result_list) + "\" ]")
                print("[" + ",".join(result_add) + "]")

                result_list = []
                result_add = []

                index_list_ix = 0
                if s is modified_sorted_list[-1]:
                    break
        except Exception as e3:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e3.__traceback__))
            print("例外:calc_of_all_poker")
                
        index_list_ix = index_list_ix + 1
        



ending_scroll_sanka()