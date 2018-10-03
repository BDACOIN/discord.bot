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
import EnvironmentVariable


# パッケージのインポートとインスタンス作成
client = discord.Client()

# 他のモジュールへの伝搬が面倒なので、Pythonの組み込み変数同様の扱いにしてしまう
builtins.client = client


# テストサーバー用のトークン
BOT_TOKEN = EnvironmentVariable.get_discord_bot_token()


# ログイン&準備が完了したら一度だけ実行される
@client.event
async def on_ready():
    # コンソールにBOTとしてログインした名前とUSER-IDを出力
    print('Logged in as')
    print('BOT-NAME :', client.user.name)
    print('BOT-ID   :', client.user.id)
    print('------')


BDA_MEMBER_ID_DICT = {}

def get_data_kaiwa_post_path(message, id):
    return 'DataMemberPostInfo/' + str(id) + ".json"


def get_user_id_from_fullname(fullname):


    # まだ未格納であれば
    if len(BDA_MEMBER_ID_DICT) == 0:
        # BDAサーバーの本来のサーバーの雑談チャンネル
        bda_zatsudan_channel = client.get_channel('443638843225407489')
        if bda_zatsudan_channel:
            for m in list(bda_zatsudan_channel.server.members):
                BDA_MEMBER_ID_DICT[str(m)] = m.id
                
    
    try:           
        id = BDA_MEMBER_ID_DICT[fullname]
        return id
    except:
        return "-1"
    


async def save(message, postinfo, id):
    path = get_data_kaiwa_post_path(message, id)
    print(path)
    json_data = json.dumps(postinfo, indent=4)
    with open(path, "w") as fw:
        fw.write(json_data)


# メッセージを受信するごとに実行される
@client.event
async def on_message(message):
    list_name = []
    list_name_tag = []
    list_name_xp = []

    with open("mee6.txt", "r", encoding="utf-8") as f:
        counter = 0
        line = f.readline()

        while line:
            line = line.strip()
            if counter % 7 == 0:
                pass
            if counter % 7 == 1:
                list_name.append(line)
            if counter % 7 == 2:
                list_name_tag.append(line)
            if counter % 7 == 3:
                m = re.search("\((\d+) tot\.\)", line)
                list_name_xp.append(int(m.group(1)))
            if counter % 7 == 4:
                pass
            if counter % 7 == 5:
                pass
            if counter % 7 == 6:
                pass
                
            line = f.readline()
            counter = counter + 1



    for i in range(0, len(list_name)):

        postinfo = {
            "id": 0,
            "posthistory": [],
            "exp": 0,
        }

        username = list_name[i] + list_name_tag[i]
        id = get_user_id_from_fullname(username)
        userex = list_name_xp[i]
        print(username + ":" + str(id) + ":" + str(userex))
        postinfo["id"] = id
        postinfo["posthistory"] = []
        postinfo["exp"] = userex
        await save(message, postinfo, id)
        
    #print (list_name)
    #print (list_name_tag)
    #print (list_name_xp)

# APP(BOT)を実行
client.run(BOT_TOKEN)
