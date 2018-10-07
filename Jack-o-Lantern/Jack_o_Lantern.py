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

from PIL import Image
from PIL import ImageDraw

import EnvironmentVariable
import poker


def get_poker_cache_count_channel(member):
    for ch in member.server.channels:
        if "ポーカー" in str(ch) and "キャッシュ" in str(ch):
            return ch
            
    return None




# ２つのテキストの類似度の比較
def get_sequence_matcher_coef(test_1, text_2):

    # unicodedata.normalize() で全角英数字や半角カタカナなどを正規化する
    normalized_str1 = unicodedata.normalize('NFKC', test_1)
    normalized_str2 = unicodedata.normalize('NFKC', text_2)

    # 類似度を計算、0.0~1.0 で結果が返る
    s = difflib.SequenceMatcher(None, normalized_str1, normalized_str2).ratio()
    # print( "match ratio:" + str(s))
    return s





# テストサーバー用のトークン
BOT_TOKEN = EnvironmentVariable.get_discord_bot_token()

# パッケージのインポートとインスタンス作成
client = discord.Client()

# 他のモジュールへの伝搬が面倒なので、Pythonの組み込み変数同様の扱いにしてしまう
builtins.client = client

TRICK_OR_TREAT_TIME = False
TRICK_OR_TREAT_CHANNEL = None
# 
TRICK_OR_TREAT_TIME_POKER_REGIST_LIST = {}

# ログイン&準備が完了したら一度だけ実行される
@client.event
async def on_ready():

    global TRICK_OR_TREAT_CHANNEL

    # コンソールにBOTとしてログインした名前とUSER-IDを出力
    print('Logged in as')
    print('BOT-NAME :', client.user.name)
    print('BOT-ID   :', client.user.id)
    print('------')
    
    target_server_id = '443637824063930369' # BDA
    
    if "Test" in client.user.name:
        target_server_id = '411022327380180992' # こみやんま本舗
    
    target_server_obj = None
    try:
        for svr in client.servers:
            print(svr.id)
            if target_server_id == svr.id:
                target_server_obj = svr
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
        print("例外:poker hand_percenteges error")

    if target_server_obj:
        print("サーバー発見")
        while(True):
            target_channel_name = ["雑談", "jack-o-lantern", "trick-or-treat", "candle" ]
            try:
                print(target_channel_name)
                random_channel_name = random.choice(target_channel_name)
                target_channel_obj = None
                for c in target_server_obj.channels:
                    if c.name in target_channel_name:
                        target_channel_obj = c
                        
                if target_channel_obj:

                    em = discord.Embed(title="", description="", color=0x36393f)
                    ret_message = await client.send_message(target_channel_obj, embed=em)

                    for r in range(0, random.randint(1, 3)):
                        hmm_list = ["What...!?", "Hmm...!?", "Sweet...!?", "Well...!?", "Um...!?", "Huh...!?", "No way...!?", "Terrible...!?" ]
                        hmm = random.choice(hmm_list)
                        em.set_image(url=get_jack_o_lantern_to_r_direction(svr))
                        em.set_footer(text=hmm)
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_l_direction(svr))
                        trc_list = ["T...?", "Tr...?", "Tri...?", "Tric...?" ]
                        trc = random.choice(trc_list)
                        em.set_footer(text=trc)
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                    if random.random() < 0.7:
                        em.set_image(url=get_jack_o_lantern_trick_or_treat(svr))
                        em.set_footer(text=" ")
                        await client.edit_message(ret_message, embed=em)
                        TRICK_OR_TREAT_CHANNEL = target_channel_obj
                        # 万が一のときんためにtryしておく
                        try:
                            # await client.send_message(target_channel_obj, ":regional_indicator_t: :regional_indicator_r: :regional_indicator_i: :regional_indicator_c: :regional_indicator_k:\n                    :regional_indicator_o: :regional_indicator_r:\n          :regional_indicator_t: :regional_indicator_r: :regional_indicator_e: :regional_indicator_a: :regional_indicator_t:")
                            await asyncio.sleep(20)
                            await client.send_message(target_channel_obj, ":regional_indicator_c: :regional_indicator_l: :regional_indicator_o: :regional_indicator_s: :regional_indicator_e:")
                            TRICK_OR_TREAT_CHANNEL = None
                        except:
                            TRICK_OR_TREAT_CHANNEL = None
                            await client.send_message(target_channel_obj, ":regional_indicator_c: :regional_indicator_l: :regional_indicator_o: :regional_indicator_s: :regional_indicator_e:")
                    else:
                        TRICK_OR_TREAT_CHANNEL = None
                        damn_list = ["Bye...", "Damn...", "Shit...", "Dark...", "Gloomy...", "Dim...", "Low..." ]
                        damn = random.choice(damn_list)
                        em.set_footer(text=damn)
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)
                        await client.delete_message(ret_message)
                        
                    

                print("スリープ")
                await asyncio.sleep(25)
                TRICK_OR_TREAT_TIME_POKER_REGIST_LIST.clear()
            except Exception as e2:
                t, v, tb = sys.exc_info()
                print(traceback.format_exception(t,v,tb))
                print(traceback.format_tb(e2.__traceback__))
                print("例外:poker hand_percenteges error")
                await asyncio.sleep(25)
                TRICK_OR_TREAT_TIME_POKER_REGIST_LIST.clear()


def get_jack_o_lantern_to_r_direction(server):
    if '443637824063930369' in server.id:
        return "https://media.discordapp.net/attachments/498183493361205278/498330369213333504/jack-o-lantern-to-r-direction.png"
    else:
        return "https://media.discordapp.net/attachments/498162384716955655/498333423195389965/jack-o-lantern-to-r-direction.png"

def get_jack_o_lantern_to_l_direction(server):
    if '443637824063930369' in server.id:
        return "https://media.discordapp.net/attachments/498183493361205278/498330385764319272/jack-o-lantern-to-l-direction.png"
    else:
        return "https://media.discordapp.net/attachments/498162384716955655/498333594075267083/jack-o-lantern-to-l-direction.png"

def get_jack_o_lantern_trick_or_treat(server):
    if '443637824063930369' in server.id:
        return "https://media.discordapp.net/attachments/498183493361205278/498330403447504897/trick_or_treat.png"
    else:
        return "https://media.discordapp.net/attachments/498162384716955655/498334187565350934/trick_or_treat.png"


async def send_typing_message(channel, text):
    text_len = len(text)
    if text_len > 5:
        text_len = text_len - 5
    text_len = text_len / 30
    if text_len >= 1.5:
        text_len = 1.5

    #await client.send_typing(channel)
    #await asyncio.sleep(text_len)
    await client.send_message(channel, text)


client.send_typing_message = send_typing_message


def get_hand_names():
    '''
    Sample n random hands and print a table of percentages for each type of hand.
    '''
    hand_names =('ブタ -High Card-', 'ワンペア -1 Pair-', 'ツーペア -2 Pairs-', 'スリーカード -3 Kind-', 'ストレート -Straight-', 'フラッシュ -Flush-', 'フルハウス -Full House-', 'フォーカード -4 Kind-', 'ストレートフラッシュ -Straight Flush-')
    return hand_names


# ベストの役が計算された並びをもとに、元のオリジナルのジョーカーなどがある
# (かもしれない)カード名へと戻す
def best_wild_hand_reflect_hands(cards, bests):

    rests = cards[:]

    displays_cards = []
    
    # 最終的な手札の並びに基づいて…
    for b in bests:
        # それが元のカードにあれば
        if b in rests:
            # その最終的な手札のならびに従ってリストに加える
            displays_cards.append(b)
            
        # 元のカードにないということはジョーカー
        # 最終的なジャッジが黒系カード(スペードかクラブ)なら
        # 黒のジョーカーが代用となった
        elif "S" in b or "C" in b:
            displays_cards.append("WJB")

        # 元のカードにないということはジョーカー
        # 最終的なジャッジが赤系カード(ハードかダイヤ)なら
        # 赤のジョーカーが代用となった
        elif "H" in b or "D" in b:
            displays_cards.append("WJR")
            
        rests.pop(0)

    return displays_cards

def get_all_cards():
    black_joker_cards = [r+s for r in '23456789TJQKA' for s in 'SC']
    red_joker_cards = [r+s for r in '23456789TJQKA' for s in 'HD']
    jokers = ['?B', '?R']

    all_cards = []
    all_cards.extend(jokers)
    all_cards.extend(black_joker_cards)
    all_cards.extend(red_joker_cards)
    return all_cards
    

def make_png_img(message, displays_cards):
    base = Image.open("card/ZBASE.png")

    x = 0
    for c in displays_cards:
        card_img = Image.open("card/" + c + ".png")
        base.paste(card_img, (x,0))
        x = x + card_img.width

    # base.save("aaa.png")

    # 現在のunixタイムを出す
    now = datetime.datetime.now()
    unix = now.timestamp()
    unix = int(unix)
    
    path2 = str(unix) + "_" + str(message.id) + "_poker" + ".png"
    path = "DataTempImage/" + path2
    base.save(path)
    ### aaa = Image.alpha_composite(black, green)
    # layers = Image.alpha_composite(black, frame)
    # layers.save("level_up_image_{0:03d}".format(i)+ ".png")
    return path, path2


def get_symbol_display_cards(cards):
    midifiled_cards = []
    for c in cards:
        c = c.replace("WJB", "Jo(B)")
        c = c.replace("WJR", "Jo(R)")
        c = c.replace("S", "♤")
        c = c.replace("D", "♢")
        c = c.replace("H", "♡")
        c = c.replace("C", "♧")
        c = c.replace("T", "10")
        midifiled_cards.append(c)
        
    return midifiled_cards
    



def get_url_of_hallowine_cards_base(message):
    if "BDA" in message.channel.server.name:
        return "https://media.discordapp.net/attachments/498183493361205278/498183608679268359/hallowine_cards_base.png"
    else:
        return "https://media.discordapp.net/attachments/498162384716955655/498184214886481950/hallowine_cards_base.png"

async def member_hand_percenteges(message):
    
    global TRICK_OR_TREAT_CHANNEL
    # 入力タイミングではない
    if not TRICK_OR_TREAT_CHANNEL:
        return False
    
    # チャンネルが違う
    if TRICK_OR_TREAT_CHANNEL.id != message.channel.id:
        return False
        
    # ハッピーハロウィンの言葉的なものを入力してる？
    if not IsInputHappyHalloWeenWords(message.content):
        return False
    
    # もう入力済み
    if message.author.id in TRICK_OR_TREAT_TIME_POKER_REGIST_LIST:
        print("入力済み")
        print(str(TRICK_OR_TREAT_TIME_POKER_REGIST_LIST))
        return False
    
    hand_names = get_hand_names()

    # cards = message.content.split()
    
    all_cards = get_all_cards()
    # 5枚をランダムに
    cards = random.sample(all_cards, 5)
    
    bests = poker.best_wild_hand(cards)

    display_cards = best_wild_hand_reflect_hands(cards, bests)
    path, path2 = make_png_img(message, display_cards)
    rank = poker.hand_rank(bests)

    modified_display_cards = get_symbol_display_cards(display_cards)
    str_tehuda = "  ,  ".join(modified_display_cards)

    TRICK_OR_TREAT_TIME_POKER_REGIST_LIST[message.author.id] = bests

#    f = discord.File(path, filename=path2)
    cache_channel = get_poker_cache_count_channel(message.author)
    print("★チャンネル情報" + str(cache_channel))
    content_message = "..."
    send_message_obj = await client.send_file(cache_channel, path, content=content_message, filename=path2)
    
    try:
        em = discord.Embed(title="", description="", color=0xDEED33)
        em.add_field(name="ハロウィンポーカー -The Halloween in Poker-", value= "<@" + message.author.id + ">", inline=False)
        str_tehuda = "  ,  ".join(modified_display_cards)
        em.add_field(name=hand_names[rank[0]], value=str_tehuda, inline=True)
        avator_url = message.author.avatar_url or message.author.default_avatar_url
        avator_url = avator_url.replace(".webp?", ".png?")
        em.set_thumbnail(url=avator_url)

        em.set_image(url=get_url_of_hallowine_cards_base(message))
            
        ret = await client.send_message(message.channel, embed=em)
        proxy_url = send_message_obj.attachments[0]["proxy_url"]
        await asyncio.sleep(2)
        em.set_image(url=proxy_url)
        await client.edit_message(ret, embed=em)
        await asyncio.sleep(10)
        await client.delete_message(send_message_obj)
        
        return True

    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
        print("例外:poker hand_percenteges error")



def delete_old_image(message):
    print("delete_old_image")

    files = os.listdir('DataTempImage')
    for file in files:
        print(file)
        try:
            m = re.search("^[0-9]+", file)
            print(str(m))
            date = m.group(0)
            print(date)
            date = int(date)
            
            # 現在のunixタイムを出す
            now = datetime.datetime.now()
            unix = now.timestamp()
            unix = int(unix)

            if unix-date > 60:
                os.remove('DataTempImage/' + file)
            print (unix - date)
            
        except:
            print(sys.exc_info())



# ハッピーハロウィンの文言を入力したのか？
def IsInputHappyHalloWeenWords(text):
    similar1 = get_sequence_matcher_coef(text, "Happy Halloween!")
    similar2 = get_sequence_matcher_coef(text, "ハッピーハロウィン")
    similar3 = get_sequence_matcher_coef(text, "はっぴーはろうぃん")
    similar4 = get_sequence_matcher_coef(text, "ハッピーはろうぃん")
    similar5 = get_sequence_matcher_coef(text, "はっぴーハロウィン")
    similar6 = get_sequence_matcher_coef(text, "ﾊｯﾋﾟｰﾊﾛｳｨﾝ")
    if similar1 > 0.5 or similar2 > 0.5 or similar3 > 0.5 or similar4 > 0.5 or similar5 > 0.5 or similar6 > 0.5:
        return True
    else:
        return False


G_LASTEST_DELETE_TIMESTAMP = 0

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

        is_success = await member_hand_percenteges(message)

    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
        print("例外:poker hand_percenteges error")


    try:

        delete_old_image(message)
            
    except Exception as e:
        pass

# APP(BOT)を実行
client.run(BOT_TOKEN)
