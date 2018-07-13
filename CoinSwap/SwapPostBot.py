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
import sys
import datetime
import time
import discord


import EnvironmentVariable
import JudgeErrorWalletAddress
import WavesJsonToPythonObj
import GetWavesNodeTransaction
import SearchWavesTransactionFromAddress


# テストサーバー用のトークン
BOT_TOKEN = EnvironmentVariable.get_discord_bot_token()



# パッケージのインポートとインスタンス作成
client = discord.Client()

# 他のモジュールへの伝搬が面倒なので、Pythonの組み込み変数同様の扱いにしてしまう
builtins.client = client


# ログイン&準備が完了したら一度だけ実行される
@client.event
async def on_ready():
    # コンソールにBOTとしてログインした名前とUSER-IDを出力
    print('Logged in as')
    print('BOT-NAME :', client.user.name)
    print('BOT-ID   :', client.user.id)
    print('------')



def makedir_and_file(ret):
    dirpath = ret["eth_address"]
    dirpath = dirpath.strip()
    if "eth_status" in ret and ret["eth_status"] == "error":
        return False
    try:
        os.mkdir("postdata/"+dirpath)
    except:
        pass

    filename = ret["transaction_id"]
    f = open("postdata/" + dirpath + "/" + filename + ".txt", "w")
    json_data = json.dumps(ret, indent=4)
    f.write(json_data)
    f.close()

    return True


# メッセージを受信するごとに実行される
@client.event
async def on_message(message):

    # BOTとメッセージの送り主が同じ人なら処理しない
    if client.user == message.author:
        return
    
    # 送信主がBOTなら処理しない
    roles = message.author.roles
    for r in roles:
        if r.name == "BOT":
            return

    mention_msg = "{0.author.mention}".format(message)

    if str(message.channel) == "erc申請":
        msg = message.content.strip()
        if JudgeErrorWalletAddress.is_message_ether_pattern(msg):
            await client.send_message(message.channel, mention_msg + "\nEther ウォレットアドレス ではなく、\nWaves の **Transaction ID** を投稿してください。")

        elif JudgeErrorWalletAddress.is_message_waves_pattern(msg):
            if msg == WavesJsonToPythonObj.recipient_wallet_address_of_BDA:
                await client.send_message(message.channel, mention_msg + "\nそのアドレスは BDA Waves の送金先のウォレットアドレスです。")
            else:
                info = SearchWavesTransactionFromAddress.search_waves_transaction_from_address(msg)
                await client.send_message(message.channel, mention_msg + "\nWaves ウォレットアドレス ではなく、\nWaves の **Transaction ID** を投稿してください。")
                for ret in info:
                    makedir_and_file(ret)
                    await client.send_message(message.channel, str(ret))

        elif GetWavesNodeTransaction.is_waves_transaction_regex_pattern(msg):
            # wavesアドレスを元に、直近のトランザクション全部を引き出す
            str_json = GetWavesNodeTransaction.get_waves_node_transaction_json(msg)

            ret = WavesJsonToPythonObj.json_to_python_obj(str_json)
            if "status" in ret and ret["status"] == "error":
                await client.send_message(message.channel, mention_msg + "\n対象のWaves の **Transaction ID** の取引内容を読み取れませんでした。")
            elif "eth_status" in ret and ret["eth_status"] == "error":
                await client.send_message(message.channel, mention_msg + "\nあなたは送金において**深刻なミス**をしています!!\n**Attachmentにイーサーアドレスを記載していない**状態で、\nBDA Waves Tokenを送金しています。\n")
            else:
                makedir_and_file(ret)
                await client.send_message(message.channel, mention_msg + str(ret))

        else:
            await client.send_message(message.channel, mention_msg + "\nご投稿の内容は、ERC交換申請情報として認識できません。")

# APP(BOT)を実行
client.run(BOT_TOKEN)
