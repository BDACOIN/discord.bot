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

import copy
import asyncio


import EnvironmentVariable
import poker





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
    


async def send_typing_message(channel, text):
    text_len = len(text)
    if text_len > 5:
        text_len = text_len - 5
    text_len = text_len / 30
    if text_len >= 1.5:
        text_len = 1.5

    await client.send_typing(channel)
    await asyncio.sleep(text_len)
    await client.send_message(channel, text)


client.send_typing_message = send_typing_message




async def hand_percenteges(message):
    '''
    Sample n random hands and print a table of percentages for each type of hand.
    '''
    hand_names = ('High Card', '1 Pair', '2 Pairs', '3 Kind', 'Straight', 'Flush', 'Full House', '4 Kind', 'Straight Flush')

    best = poker.best_wild_hand(message.content.split())
    rank = poker.hand_rank(best)
    await client.send_typing_message(message.channel, str(best))
    await client.send_typing_message(message.channel, str(hand_names[rank[0]]))




# メッセージを受信するごとに実行される
@client.event
async def on_message(message):

    try:
        print(message.channel.id)
    except:
        pass

    # BOTとメッセージの送り主が同じ人なら処理しない
    if client.user == message.author:
        return

    try:
        # 送信主がBOTなら処理しない
        roles = message.author.roles;
        for r in roles:
            if r.name == "BOT":
                return
    except:
        pass

    try:

        await hand_percenteges(message)

    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
        print("例外:poker hand_percenteges error")


# APP(BOT)を実行
client.run(BOT_TOKEN)
