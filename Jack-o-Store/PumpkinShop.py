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
import asyncio
import traceback

import EnvironmentVariable



# 上記で取得したアプリのトークンを入力



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




def get_data_halloween_poker_path(message):
    id = message.author.id
    return '../Jack-o-Lantern/DataHalloweenPokerInfo/' + str(id) + ".json"


def get_pumpkin_unko_picture(server):
    if '443637824063930369' in server.id: # BDA鯖
        return "https://media.discordapp.net/attachments/498183493361205278/501761136262250496/pumpkin-unko.png"
    else:
        return "https://media.discordapp.net/attachments/498162384716955655/501758815235080202/pumpkin-unko.png"

def get_pumpkin_d9_picture(server):

    if '443637824063930369' in server.id: # BDA鯖
        return "https://media.discordapp.net/attachments/498183493361205278/506071604166656011/9D.png"
    else:
        return "https://media.discordapp.net/attachments/498162384716955655/506071314054905857/9D.png"

    

def update_one_halloween_poker_jack_unko(message, member):
    try:

        path = get_data_halloween_poker_path(message)
        # print(path)
        with open(path, "r") as fr:
            pokerinfo = json.load(fr)

        # キーがなければ作成
        if not "poop" in pokerinfo:
            pokerinfo["poop"] = []

        now = datetime.datetime.now()
        unix = now.timestamp()
        unix = int(unix)

        pokerinfo["poop"].append( {str(unix):2} )

        path = get_data_halloween_poker_path(message)
        json_data = json.dumps(pokerinfo, indent=4)
        with open(path, "w") as fw:
            fw.write(json_data)

        em = discord.Embed(title="", description="", color=0x36393f)
        em.set_image(url=get_pumpkin_unko_picture(message.channel.server))
        em.add_field(name="返信相手 (reply)", value= "<@" + member.id + ">\n何かを得たようだ... (You got something..)", inline=False)
        em.set_footer(text="「!JACK」とはなんだろう...? (What is ❝!JACK❞?)")
        
        return em

    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
    
    return False



async def load_one_halloween_poker_jack_unko(message):
    try:

        path = get_data_halloween_poker_path(message)
        with open(path, "r") as fr:
            pokerinfo = json.load(fr)
            
        count = 0
        if "poop" in pokerinfo:
            for ele in pokerinfo["poop"]:
                for e in ele:
                    if ele[e] > 0:
                        count = count + ele[e]

        return count

    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
    
    return 0


async def decrement_one_halloween_poker_jack_unko(message):
    try:

        path = get_data_halloween_poker_path(message)
        with open(path, "r") as fr:
            pokerinfo = json.load(fr)
            
        count = 0
        if "poop" in pokerinfo:
            is_falsed = False
            for ele in pokerinfo["poop"]:
                for e in ele:
                    if ele[e] > 0:
                        if not is_falsed:
                            ele[e] = ele[e] - 1
                            is_falsed = True
                        count = count + ele[e]

        path = get_data_halloween_poker_path(message)
        json_data = json.dumps(pokerinfo, indent=4)
        with open(path, "w") as fw:
            fw.write(json_data)
            
        return count

    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
    
    return 0



def get_data_memberinfo_path(message, id):
    return '../Diatan/DataMemberInfo/' + str(id) + ".json"


async def has_member_data(message, id, withMessage):
    path = get_data_memberinfo_path(message, id)
    if not os.path.exists(path):
        if withMessage:
            ch = get_ether_regist_channel(message)
            await report_error(message, "登録情報がありません。\n" + "<#" + ch.id + ">" + " に\nご自身の **MyEtherWallet** など、\nエアドロが受け取れるETHウォレットアドレスを投稿し、\n**コインを受け取れるように**してください。")
        return False
    else:
        return True


async def get_count_one_member_omikuji_data(message, id):
    try:
        has = await has_member_data(message, id, False)
        if not has:
            return 0

        path = get_data_memberinfo_path(message, id)
        print(path)
        with open(path, "r") as fr:
            memberinfo = json.load(fr)

        return memberinfo["omikuji_ticket_count"]

    except:
        await report_error(message, "get_count_one_member_omikuji_data中にエラー")
        await report_error(message, sys.exc_info())
    
    return None


async def decrement_one_member_omikuji_data(message, id):
    try:
        has = await has_member_data(message, id, False)
        if not has:
            return None

        path = get_data_memberinfo_path(message, id)
        print(path)
        with open(path, "r") as fr:
            memberinfo = json.load(fr)

        if memberinfo["omikuji_ticket_count"] <= 0:
            print("おみくじのチケットが無い")
            return None

        memberinfo["omikuji_ticket_count"] = memberinfo["omikuji_ticket_count"] - 3

        path = get_data_memberinfo_path(message, id)
        json_data = json.dumps(memberinfo, indent=4)
        with open(path, "w") as fw:
            fw.write(json_data)

        print("チケットカウントを返す" + str(memberinfo["omikuji_ticket_count"]))
        return memberinfo["omikuji_ticket_count"]

    except:
        await report_error(message, "decrement_one_member_omikuji_data中にエラー")
        await report_error(message, sys.exc_info())
    
    return None


# 1人分のメンバーデータの作成
async def make_one_halloween_poker_data(message):
    try:
        pokerinfo = {
            "id": message.author.id,
            "cardhistory": [],
            "amount": {},
        }
        
        path = get_data_halloween_poker_path(message)
        # print("ここきた★" + path)
        json_data = json.dumps(pokerinfo, indent=4)
        with open(path, "w") as fw:
            fw.write(json_data)
        return pokerinfo
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
        await report_error(message, "make_one_halloween_poker_data 中にエラーが発生しました。")
        await report_error(message, sys.exc_info())
    return None




def get_ether_regist_channel(target_channel_obj):
    for ch in target_channel_obj.server.channels:
        if "イーサアドレス登録" in str(ch) or "eth-address" in str(ch) or "ethアドレス登録" in str(ch):
            return ch
            
    return None


def has_post_data(message):
    path = get_data_halloween_poker_path(message)
    if not os.path.exists(path):
        return False
    else:
        return True


async def report_error(message, error_msg):
    em = discord.Embed(title=" ", description="─────────\n" , color=0xDEED33)
    em.set_author(name='Jack-o-Lantern', icon_url=client.user.avatar_url)
    
    em.add_field(name="返信相手(Reply)", value= "<@" + message.author.id + ">", inline=False)
    em.add_field(name="エラー(Error)", value=error_msg, inline=False)
    try:
        print(error_msg)
        await client.send_message(message.channel, embed=em)
    except:
        print(sys.exc_info())


TARGET_MEMBER_MESSAGE = {}

@client.event
async def on_reaction_add(reaction, user):

    try:
        if reaction.message.channel.name == "カボチャの館":
            if reaction.emoji == '💩':
                if user.id in TARGET_MEMBER_MESSAGE:
                    message = TARGET_MEMBER_MESSAGE[user.id]
                    
                    has_ticket_count = await get_count_one_member_omikuji_data(message, message.author.id)
                    if has_ticket_count < 3:
                        await client.send_message(message.channel, "おみくじ券が足りないですぜー\n")
                    else:
                        await client.send_message(message.channel, "<@" + message.author.id + "> 、まいどあり！")
                        await decrement_one_member_omikuji_data(message, message.author.id)
                        em = update_one_halloween_poker_jack_unko(message, message.author)
                        ret_message = await client.send_message(message.channel, embed=em)
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
        await report_error(message, "on_reaction_add 中にエラーが発生しました。")
        await report_error(message, sys.exc_info())


# メッセージを受信するごとに実行される
@client.event
async def on_message(message):

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
        if message.channel.name == "カボチャの館":
            # ETHアドレスに登録がある。
            if not os.path.exists("../Diatan/DataMemberInfo/" + str(message.author.id) + ".json"):
                eth_ch = get_ether_regist_channel(message.channel)
                await report_error(message, "登録情報がないぜぃ？\n" + "<#" + eth_ch.id + ">" + " に\n自分の **MyEtherWallet** など、\nエアドロが受け取れるETHウォレットアドレスを投稿して、\n**コインを受け取れるように**するのがいいですぜー？")
                return

            # 一度も参戦したことが無い人は利用できない
            if not has_post_data(message):
                await report_error(message, "ここは ハロウィン・ポーカー に参加したことがある人向けのショップですぜ～")
                return

            message_upper = message.content.upper()
            if "CARD" in message_upper or "カード" in message_upper or "かーど" in message_upper:
                TARGET_MEMBER_MESSAGE[message.author.id] = message

                avator_url = client.user.avatar_url or client.user.default_avatar_url
                print(avator_url)
                avator_url = avator_url.replace(".webp?", ".png?")

                em = discord.Embed(title="", description="", color=0x36393f)
                em.set_image(url=get_pumpkin_d9_picture(message.channel.server))
                em.add_field(name="返信相手 (reply)", value= "<@" + message.author.id + "> このカードですかい？", inline=False)
                em.add_field(name="交換条件", value= "　幸運のおみくじ券 ３枚", inline=False)
                em.set_footer(text="買うときゃウンコでスタンプしてくだせぇ～")
                # em.set_thumbnail(url="https://media.discordapp.net/attachments/498183493361205278/506094216657502209/thumb.png")

                ret_message = await client.send_message(message.channel, embed=em)
                await asyncio.sleep(3)
                await client.add_reaction(ret_message, "💩")
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
        await report_error(message, "on_message 中にエラーが発生しました。")
        await report_error(message, sys.exc_info())

# APP(BOT)を実行
client.run(BOT_TOKEN)
