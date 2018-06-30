#coding: utf-8

import types
import os
import sys, datetime, time
import discord
import asyncio

# 上記で取得したアプリのトークンを入力

# BDA / COINのサーバー
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", r'****************************************')

# パッケージのインポートとインスタンス作成
client = discord.Client()

# グローバル
myTime = 0
OtsuStart = False
TargetChannel = 0


# ログイン&準備が完了したら一度だけ実行される
@client.event
async def on_ready():
    # コンソールにBOTとしてログインした名前とUSER-IDを出力
    print('Logged in as')
    print('BOT-NAME :', client.user.name)
    print('BOT-ID   :', client.user.id)
    print('------')

    # グローバルでやりとりしてるので宣言
    global myTime
    global OtsuStart
    global TargetChannel
    
    
    OtsuDoneList = [1,2,3]
    while True:

        # 0.5秒に一度のチェック
        await asyncio.sleep(0.5)

        # 処理途中に妙に時間変化したりしないようにここで
        constTime = int(time.time())
        print(constTime)
        for server in OtsuDoneList:
            if not OtsuStart:
                timeState = 0
                break

            if timeState == 0 and myTime+15 < constTime:
                timeState = 1
                print("まんなか")
                await client.send_message(TargetChannel, "真ん中")

            if timeState == 1 and myTime+25 < constTime:
                timeState = 2
                print("５秒前")
                await client.send_message(TargetChannel, "５秒前")
                
            if timeState == 2 and myTime+30 < constTime:
                timeState = 3
                OtsuStart = False;
                print("おわり")
                await client.send_message(TargetChannel, "終わり")


    print("on_ready_end") # ← 来ないはず


# メッセージを受信するごとに実行される
@client.event
async def on_message(message):

    # グローバルでやりとりしてるので宣言
    global OtsuStart
    global myTime
    global TargetChannel

    # 定期掲載があったらスタートするっていうのの簡易
    # OtsuStartの2重は危険
    if not OtsuStart:
    
        # 定期掲載を受けてキック
        if "定期再掲" in message.content:
            await client.send_message(message.channel, "otsustart")

        # 自分自身の投稿を感じてスタート
        if "otsustart" in message.content:
            print("otsustart")
            OtsuStart = True
            myTime = time.time()
            TargetChannel = message.channel # チャンネルの保持

        

# APP(BOT)を実行
client.run(BOT_TOKEN)

