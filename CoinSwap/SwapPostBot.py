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
import CalcTargetEatherInfo


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


def GetEmbeddedReportOneTransaction(message, ret):
    if "status" in ret and ret["status"] == "error":
        # await client.send_message(message.channel, mention_msg + "\n対象のWaves の **Transaction ID** の取引内容を読み取れませんでした。")

        em = discord.Embed(title="", description="", color=0xDEED33)
        em.set_thumbnail(url="http://bdacoin.org/bot/coinswap/image/error.png")
        em.add_field(name="返信相手", value="<@" + message.author.id + ">", inline=False)
        em.add_field(name="ステータス", value="登録失敗", inline=False)
        if "asset_error" in ret:
            em.add_field(name="捕捉", value="対象のWaves の **Transaction ID** はBDA送金ではありません。", inline=False)
            return em
        else:
            em.add_field(name="捕捉", value="対象のWaves の **Transaction ID** の取引内容を読み取れませんでした。", inline=False)
            return em

    elif ("eth_status" in ret and ret["eth_status"] == "error") or ("user_id" in ret and ret["user_id"] == 0):
        
        em = discord.Embed(title="", description="", color=0xDEED33)
        em.set_thumbnail(url="http://bdacoin.org/bot/coinswap/image/error.png")
        em.add_field(name="返信相手", value="<@" + message.author.id + ">", inline=False)
        em.add_field(name="ステータス", value="登録失敗", inline=False)
        em.add_field(name="Transaction ID", value=str(ret["transaction_id"]), inline=False)
        em.add_field(name="Transaction IDの内容", value="https://wavesexplorer.com/tx/" + str(ret["transaction_id"]), inline=False)
        em.add_field(name="このTransactionでのBDA(Waves版)の送金枚数", value=str(ret["amount"]) + " 枚", inline=False)
        if ("eth_status" in ret and ret["eth_status"] == "error"):
            em.add_field(name="受取用のETHウォレットのアドレス", value="\nこのTransactionは送金において**深刻なミス**をしています!!\n**Attachment(Description)に、\nイーサーウォレットアドレスを記載していない**状態で、\nBDA(Waves版)を送金されています。\n", inline=False)
        else:
            em.add_field(name="受取用のETHウォレットのアドレス", value=str(ret["eth_address"]), inline=False)
        if ("user_id" in ret and ret["user_id"] == 0):
            em.add_field(name="送金者識別番号", value="\nこのTransactionは送金において**深刻なミス**をしています!!\n**Attachment(Description)に、\n送金者識別番号を記載していない**状態で、\nBDA(Waves版)を送金されています。\n", inline=False)
        else:
            em.add_field(name="送金者識別番号", value=str(ret["user_id"]))
        
        em.add_field(name="このTransactionでのアタッチメントに記載された内容", value=str(ret["attachment"]), inline=False)
        em.add_field(name="受取予定となるBDA(ERC版)の枚数", value="0 枚", inline=False)
        return em

        
    else:
        # await client.send_message(message.channel, mention_msg + str(ret))

        em = discord.Embed(title="", description="", color=0xDEED33)
        em.add_field(name="返信相手", value="<@" + message.author.id + ">", inline=False)

        if str(int(ret["user_id"])) == str(int(message.author.id)):
            makedir_and_file(ret)
            em.set_thumbnail(url="http://bdacoin.org/bot/coinswap/image/ok.png")
            em.add_field(name="ステータス", value="登録成功", inline=False)
            em.add_field(name="Transaction ID", value=str(ret["transaction_id"]), inline=False)
            em.add_field(name="Transaction IDの内容", value="https://wavesexplorer.com/tx/" + str(ret["transaction_id"]), inline=False)
            em.add_field(name="このTransactionでのBDA(Waves版)の送金枚数", value=str(ret["amount"]) + " 枚", inline=False)
            em.add_field(name="受取用のETHウォレットのアドレス", value=str(ret["eth_address"]), inline=False)
            em.add_field(name="受取予定となるBDA(ERC版)の枚数", value=str(ret["eth_amount"]) + " 枚", inline=False)
            return em
        else:
            em.set_thumbnail(url="http://bdacoin.org/bot/coinswap/image/error.png")
            em.add_field(name="ステータス", value="登録失敗", inline=False)
            em.add_field(name="Transaction ID", value=str(ret["transaction_id"]), inline=False)
            em.add_field(name="Transaction IDの内容", value="https://wavesexplorer.com/tx/" + str(ret["transaction_id"]), inline=False)
            em.add_field(name="送金者識別番号", value="送金者識別番号が、あなたと一致していません。", inline=False)
            return em



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

    if str(message.channel) == "①コメントの取得":
        msg = message.content.strip()
        if JudgeErrorWalletAddress.is_message_ether_pattern(msg):
            em = discord.Embed(title="", description="", color=0xDEED33)
            em.add_field(name="返信相手", value="<@" + message.author.id + ">\n送金する際、\n" +
            "以下の内容をAttachment(Description)に**必ず正しく記載**してください。\n", inline=False)
            em.add_field(name="Attachment(Description)に記載する内容", value=msg+","+str(int(str(message.author.id))), inline=False)
            
            await client.send_message(message.channel, embed=em)
        else:
            await client.send_message(message.channel, mention_msg + "\nご投稿の内容は、イーサウォレットアドレスのパターンとして認識できません。")

    elif str(message.channel) == "③受取予定枚数の確認":
        msg = message.content.strip()
        if JudgeErrorWalletAddress.is_message_ether_pattern(msg):
            ret = CalcTargetEatherInfo.GetEtherWillSendAmount(msg)
            print(ret)
            # そんなアドレスの情報は無い
            em = discord.Embed(title="", description="", color=0xDEED33)
            if ret == []:
                em.set_thumbnail(url="http://bdacoin.org/bot/coinswap/image/error.png")
                em.add_field(name="イーサアドレス", value=msg + "\nに関する情報はありません。", inline=False)

            else:
                user_id_list = ret["user_id_list"]
                post_user_id = int(message.author.id)
                print(post_user_id)
                print(user_id_list)
                match_user_id_list = filter(lambda id:id==post_user_id, user_id_list )
                print(match_user_id_list)
                match_user_id_list = list(match_user_id_list)
                print(len(match_user_id_list))
                # 全くマッチしない
                if len(match_user_id_list) == 0:
                    em.set_thumbnail(url="http://bdacoin.org/bot/coinswap/image/error.png")
                    em.add_field(name="返信相手", value="<@" + message.author.id + ">", inline=False)
                    em.add_field(name="イーサアドレス", value=msg + "\nはあなたに紐づいていません。", inline=False)

                # １つでもマッチしたら、該当のイーサーアドレスに関する情報は全て見る権利があると言えるだろう。
                else:
                    em.set_thumbnail(url="http://bdacoin.org/bot/coinswap/image/ok.png")
                    em.add_field(name="返信相手", value="<@" + message.author.id + ">", inline=False)
                    em.add_field(name="イーサアドレス", value=msg + "\nに関する情報です。", inline=False)
                    em.add_field(name="該当アドレスのBDA(ERC版)受取予定枚数", value=str(ret["eth_amount"]) +" 枚", inline=False)

                
            await client.send_message(message.channel, embed=em)
        else:
            await client.send_message(message.channel, mention_msg + "\nご投稿の内容は、イーサウォレットアドレスのパターンとして認識できません。")

    elif str(message.channel) == "②トランザクションの申請":
        msg = message.content.strip()
        if JudgeErrorWalletAddress.is_message_waves_pattern(msg):
            if msg == WavesJsonToPythonObj.recipient_wallet_address_of_BDA:
                em = discord.Embed(title="", description="", color=0xDEED33)
                em.set_thumbnail(url="http://bdacoin.org/bot/coinswap/image/error.png")
                em.add_field(name="返信相手", value="<@" + message.author.id + ">", inline=False)
                em.add_field(name="エラー", value="そのアドレスは BDA(Waves版)の運営ウォレットアドレスです。", inline=False)
                await client.send_message(message.channel, embed=em)
            else:
                info = SearchWavesTransactionFromAddress.search_waves_transaction_from_address(msg)
                if len(info) == 0:
                    await client.send_message(message.channel, mention_msg + "\nご投稿のウォレットアドレスから運営ウォレットへと\nBDA(Waves版)を送金している**Transaction ID**は発見できませんでした。")
                else:
                    await client.send_message(message.channel, mention_msg + "\n以下は、ご投稿のウォレットアドレスから運営ウォレットへと\nBDA(Waves版)を送金している**Transaction ID**一覧候補となります。")
                    for ret in info:
                        em = GetEmbeddedReportOneTransaction(message, ret)
                        await client.send_message(message.channel, embed=em)

#                        em = discord.Embed(title="", description="", color=0xDEED33)
#                        em.add_field(name="返信相手", value="<@" + message.author.id + ">", inline=False)
#                        em.add_field(name="Transaction ID", value=str(ret["transaction_id"]), inline=False)
#                        em.add_field(name="Transaction IDの内容", value="https://wavesexplorer.com/tx/" + str(ret["transaction_id"]), inline=False)
#                        if "eth_status" in ret and ret["eth_status"] == "error":
#                            em.set_thumbnail(url="http://bdacoin.org/bot/coinswap/image/error.png")
#                            em.add_field(name="受取用のETHウォレットのアドレス", value="\nこのTransactionは送金において**深刻なミス**をしています!!\n**Attachment(Description)に、\nイーサーウォレットアドレスを記載していない**状態で、\nBDA(Waves版)を送金されています。\n", inline=False)
#                            em.add_field(name="このTransactionでのアタッチメントに記載された内容", value=str(ret["attachment"]), inline=False)
#                        elif "user_id" in ret and ret["user_id"] == 0:
#                            em.set_thumbnail(url="http://bdacoin.org/bot/coinswap/image/error.png")
#                            em.add_field(name="送金者識別番号", value="\nこのTransactionは送金において**深刻なミス**をしています!!\n**Attachment(Description)に、\n送金者識別番号を記載していない**状態で、\nBDA(Waves版)を送金されています。\n", inline=False)
#                            em.add_field(name="このTransactionでのアタッチメントに記載された内容", value=str(ret["attachment"]), inline=False)
#                        else:
#                            em.set_thumbnail(url="http://bdacoin.org/bot/coinswap/image/ok.png")
#                        await client.send_message(message.channel, embed=em)

        elif GetWavesNodeTransaction.is_waves_transaction_regex_pattern(msg):
            # wavesアドレスを元に、直近のトランザクション全部を引き出す
            str_json = GetWavesNodeTransaction.get_waves_node_transaction_json(msg)

            ret = WavesJsonToPythonObj.json_to_python_obj(str_json)

            em = GetEmbeddedReportOneTransaction(message, ret)
            await client.send_message(message.channel, embed=em)

        else:
            await client.send_message(message.channel, mention_msg + "\nご投稿の内容は、トランザクション申請情報として認識できません。")

# APP(BOT)を実行
client.run(BOT_TOKEN)
