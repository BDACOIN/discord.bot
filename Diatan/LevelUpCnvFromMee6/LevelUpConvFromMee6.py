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

# テストサーバー用のトークン
BOT_TOKEN = EnvironmentVariable.get_discord_bot_token()


async def on_ready():
    # コンソールにBOTとしてログインした名前とUSER-IDを出力
    print('Logged in as')
    print('BOT-NAME :', client.user.name)
    print('BOT-ID   :', client.user.id)
    print('------')


list_name = []
list_name_tag = []
list_name_xp = []

with open("a.txt", "r", encoding="utf-8") as f:
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


postinfo = {
    "id": 0,
    "posthistory": [],
    "exp": 0,
}

print (list_name)
print (list_name_tag)
print (list_name_xp)

BDA_MEMBER_ID_DICT = {}

def get_user_id_from_fullname(fullname):
    # まだ未格納であれば
    if len(BDA_MEMBER_ID_DICT) == 0:
        # BDAサーバーの本来のサーバーの雑談チャンネル
        bda_zatsudan_channel = client.get_channel('443638843225407489')
        if bda_zatsudan_channel:
            for m in bda_zatsudan_channel.server.members:
                BDA_MEMBER_ID_LIST[str(m)] = m.id
                
    
    try:           
        id = BDA_MEMBER_ID_LIST[fullname]
        return id
    except:
        return "-99999"
    


#アタッチメントや画像を評価
#文字数の長さを例の関数で図って、そこで頭をカット
# !memberinfo の登録情報の右側のアイコンは本人のものを表示すべき。
# !levelupと同じもの
# コインが受け取れるよう登録申請をしてください。→コインが受け取れるようにしてください。


# APP(BOT)を実行
client.run(BOT_TOKEN)
