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
import glob


import EnvironmentVariable
import JudgeErrorWalletAddress
import WavesJsonToPythonObj
import GetWavesNodeTransaction
import SearchWavesTransactionFromAddress
import CalcTargetEatherInfo
import Base58DecodedWalletAddress

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
        print("いいい" + str(ret))
       
        em = discord.Embed(title="", description="", color=0xDEED33)
        em.set_thumbnail(url="http://bdacoin.org/bot/coinswap/image/error.png")
        em.add_field(name="返信相手", value="<@" + message.author.id + ">", inline=False)
        em.add_field(name="ステータス", value="登録失敗", inline=False)
        em.add_field(name="Transaction ID", value=str(ret["transaction_id"]), inline=False)
        em.add_field(name="Transaction IDの内容", value="https://wavesexplorer.com/tx/" + str(ret["transaction_id"]), inline=False)
        em.add_field(name="このTransactionでのBDA(Waves版)の送金枚数", value=str(ret["amount"]) + " 枚", inline=False)
        if ("eth_status" in ret and ret["eth_status"] == "error"):
            print("ooo")
            em.add_field(name="受取用のETHウォレットのアドレス", value="\nAttachmentに未記載。重大エラーです。\n", inline=False)
        else:
            print("かかか")
            em.add_field(name="受取用のETHウォレットのアドレス", value=str(ret["eth_address"]), inline=False)
        if ("user_id" in ret and ret["user_id"] == 0):
            em.add_field(name="送金者識別番号", value="\nAttachmentに未記載。重大エラーです。\n", inline=False)
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
            em.add_field(name="このTransactionでのBDA(Waves版)の送金枚数", value=str(ret["amount"]) + " 枚", inline=False)
            em.add_field(name="受取用のETHウォレットのアドレス", value=str(ret["eth_address"]), inline=False)
            em.add_field(name="受取予定となるBDA(ERC版)の枚数", value=str(ret["eth_amount"]) + " 枚", inline=False)
            return em
        else:
            em.set_thumbnail(url="http://bdacoin.org/bot/coinswap/image/error.png")
            em.add_field(name="ステータス", value="登録失敗", inline=False)
            em.add_field(name="Transaction ID", value=str(ret["transaction_id"]), inline=False)
            em.add_field(name="Transaction IDの内容", value="https://wavesexplorer.com/tx/" + str(ret["transaction_id"]), inline=False)
            print(str(ret))
            em.add_field(name="このTransactionでのアタッチメントに記載された内容", value=str(ret["attachment"]), inline=False)
            em.add_field(name="送金者識別番号", value="送金者識別番号が、あなたと一致していません。", inline=False)
            return em



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
    
    # 送信主がBOTなら処理しない
    try:
        roles = message.author.roles
        for r in roles:
            if r.name == "BOT":
                return
    except:
        pass

    mention_msg = "{0.author.mention}".format(message)

    # komiyamma
    if message.author.id == "397238348877529099":
        # そのチャンネルに存在するメッセージを全て削除する
        if message.content.startswith('!!!clear'):
            tmp = await client.send_message(message.channel, 'チャンネルのメッセージを削除しています')
            try:
                async for msg in client.logs_from(message.channel):
                    await client.delete_message(msg)
            except:
                print("削除中にエラーが発生しました")
            return

    if str(message.channel) == "①添付情報の取得" or str(message.channel) == "①get-attachment-from-bot":
        msg = message.content.strip()
        if msg == "0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA":
            await client.send_message(message.channel, mention_msg + "\nそれは概要書等に記載されていた便宜上の仮想のイーサウォレットアドレスです。")
        elif msg == "3PBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB":
            await client.send_message(message.channel, mention_msg + "\nそれは概要書等に記載されていた便宜上の仮想のWavesウォレットアドレスです。\nWavesウォレットアドレスではなく、BRD(ERC版)を受け取りたいイーサウォレットアドレスを、投稿してください。")
        elif JudgeErrorWalletAddress.is_message_ether_pattern(msg):
            em = discord.Embed(title="", description="", color=0xDEED33)
            em.add_field(name="返信相手", value="<@" + message.author.id + ">\n送金する際、\n" +
            "以下の内容をAttachment(Description)に**必ず正しく記載**してください。\n", inline=False)
            em.add_field(name="Attachment(Description)に記載する内容", value=msg+","+str(int(str(message.author.id))), inline=False)
            em.add_field(name="BDA(Waves版)の送金先", value=WavesJsonToPythonObj.recipient_wallet_address_of_BDA + " 宛てに送金してください。", inline=False)
            
            dm_msg = msg+","+str(int(str(message.author.id)))

            await client.send_message(message.channel, embed=em)
            await client.send_message(message.author, "★★必ずこれをAttachment(Description)に記載してください!!!★★")
            await client.send_message(message.author, dm_msg)
          
        elif JudgeErrorWalletAddress.is_message_waves_pattern(msg):
            await client.send_message(message.channel, mention_msg + "\nWavesウォレットアドレスではなく、BRD(ERC版)を受け取りたいイーサウォレットアドレスを、投稿してください。")
        else:
            await client.send_message(message.channel, mention_msg + "\nご投稿の内容は、イーサウォレットアドレスのパターンとして認識できません。")

    elif str(message.channel) == "③受取予定枚数の確認" or str(message.channel) == "③confirm-erc-to-be-received":
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
                    em.add_field(name="イーサアドレス", value=msg + "\nは送金者識別番号があなたと一致していません。", inline=False)

                # １つでもマッチしたら、該当のイーサーアドレスに関する情報は全て見る権利があると言えるだろう。
                else:
                    em.set_thumbnail(url="http://bdacoin.org/bot/coinswap/image/ok.png")
                    em.add_field(name="返信相手", value="<@" + message.author.id + ">", inline=False)
                    em.add_field(name="イーサアドレス", value=msg + "\nに関する情報です。", inline=False)
                    em.add_field(name="該当アドレスのBDA(ERC版)受取予定枚数", value=str(ret["eth_amount"]) +" 枚", inline=False)

                
            await client.send_message(message.channel, embed=em)
        elif JudgeErrorWalletAddress.is_message_waves_pattern(msg):
            await client.send_message(message.channel, mention_msg + "\nWavesウォレットアドレスではなく、BRD(ERC版)を受け取り申請したイーサウォレットアドレスを、投稿してください。")
        else:
            await client.send_message(message.channel, mention_msg + "\nご投稿の内容は、イーサウォレットアドレスのパターンとして認識できません。")

    elif str(message.channel) == "②トランザクションの申請" or str(message.channel) == "②regist-waves-transaction":
        msg = message.content.strip()

        if msg == "0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA":
            await client.send_message(message.channel, mention_msg + "\nそれは概要書等に記載されていた便宜上の仮想のイーサウォレットアドレスです。")

        elif msg == "3PBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB":
            await client.send_message(message.channel, mention_msg + "\nそれは概要書等に記載されていた便宜上の仮想のWavesウォレットアドレスです。")

        elif JudgeErrorWalletAddress.is_message_waves_pattern(msg):
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
                elif type(info) == type({}) and ("status" in info) and (info["status"] == "error"):
                    await client.send_message(message.channel, mention_msg + "\nご投稿のウォレットアドレスの内容を読み取ることができません。")

                else:
                    await client.send_message(message.channel, mention_msg + "\n以下は、ご投稿のウォレットアドレスから運営ウォレットへと\nBDA(Waves版)を送金している**Transaction ID**一覧候補となります。")
                    for ret in info:
                        em = GetEmbeddedReportOneTransaction(message, ret)
                        try:
                            await client.send_message(message.channel, embed=em)
                        except:
                            print(sys.exc_info())

        elif msg == WavesJsonToPythonObj.asset_id_of_BDA:
            await client.send_message(message.channel, mention_msg + "\nご投稿の内容は、BLACK DIA(Waves版)のAsset IDです。\nAsset IDではなく、送金時のご自身のWavesウォレットアドレスを投稿してください。")
        elif GetWavesNodeTransaction.is_waves_transaction_regex_pattern(msg):
            # wavesアドレスを元に、直近のトランザクション全部を引き出す
            str_json = GetWavesNodeTransaction.get_waves_node_transaction_json(msg)
            ret = WavesJsonToPythonObj.json_to_python_obj(str_json)
            em = GetEmbeddedReportOneTransaction(message, ret)
            await client.send_message(message.channel, embed=em)

        elif JudgeErrorWalletAddress.is_message_ether_pattern(msg):
            await client.send_message(message.channel, mention_msg + "\nイーサーウォレットアドレスではなく、送金時のご自身のWavesウォレットアドレスを投稿してください。")
        else:
            await client.send_message(message.channel, mention_msg + "\nご投稿の内容は、トランザクション申請情報として認識できません。")

    elif str(message.channel) == "⑩ユーザー名⇒識別番号":
        msg = message.content.strip()
        # まずは今のメンバーのところから(スワップサーバー想定)
        member_obj = discord.utils.find(lambda m: str(m) == msg, message.channel.server.members)
        if not member_obj:
            # BDAサーバーの本来のサーバーの雑談チャンネル
            bda_zatsudan_channel = client.get_channel('443638843225407489')
            if bda_zatsudan_channel:
                member_obj = discord.utils.find(lambda m: str(m) == msg, bda_zatsudan_channel.server.members)
            
        if member_obj:
            await client.send_message(message.channel, msg + " の識別番号は、\n" + str(member_obj.id))

    elif str(message.channel) == "⑪識別番号⇒ユーザー名":
        msg = message.content.strip()
        if msg.isdigit():
            await client.send_message(message.channel, msg + " の識別番号のユーザー名は、\n" + '<@' + msg + '>' )


    elif str(message.channel) == "⑫アタッチメント情報復元":
        attachment = message.content.strip()
        try:
            # base58デコードした文字列を返す。失敗した場合原文文字列ままを返す。
            base58decoded = Base58DecodedWalletAddress.get_base58_decoded_wallet_address(attachment)
            await client.send_message(message.channel, attachment+ "\n　　　↓\n" + base58decoded )
        except:
            await client.send_message(message.channel, attachment+ "\n　　　↓\n" + "変換エラー" )

    elif str(message.channel) == "⑬合格済みトランザクションチェッカー":
        msg = message.content.strip()

        glob_list = glob.glob('postdata/*/' + msg + '.txt')

        if len(glob_list) > 0:
            await client.send_message(message.channel, "該当のTransaction-ID は、__既に登録が完了しています。\n返金に応じてはいけません。__" )
        else:
            await client.send_message(message.channel, "該当のTransaction-ID は、まだ登録されていません。\n相手がまだトランザクション申請をしていないなら、\n先にトランザクション申請をしてもらい結果を確認してください。" )
        # 返金チャンネル
        henkin_list_channel = client.get_channel('474191429606834199')
        async for kako_log_msg in client.logs_from(henkin_list_channel):
            if msg in kako_log_msg.content:
                await client.send_message(message.channel, "該当のID は、__返金済です。\n返金に応じてはいけません。__" )


        
# APP(BOT)を実行
client.run(BOT_TOKEN)
