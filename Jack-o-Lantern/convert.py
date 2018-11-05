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


def get_data_halloween_poker_path(message):
    id = message.author.id
    return 'DataHalloweenPoker201810Info/' + str(id) + ".json"



def convert_one_halloween_poker_jack_unko(f):
    try:

        path = 'DataHalloweenPoker201810Info/' + f
        with open(path, "r") as fr:
            pokerinfo = json.load(fr)

        pokerinfo["amount"] = {}
        pokerinfo["cardhistory"] = []

        path = 'DataHalloweenPoker201810Info/' + f
        print(path)
        json_data = json.dumps(pokerinfo, indent=4)
        with open(path, "w") as fw:
            fw.write(json_data)

    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
    


dirlist = os.listdir("./DataHalloweenPoker201810Info")
for f in dirlist:
    print(f)
    convert_one_halloween_poker_jack_unko(f)