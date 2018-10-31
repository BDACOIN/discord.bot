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

def get_poker_result_channel(server):
    for ch in server.channels:
        if "ハロウィン・結果発表" in str(ch):
            return ch
            
    return None



def get_bgm_cache_channel(server):
    for ch in server.channels:
        if str(ch) == "halloween-bgm-cache":
            return ch
            
    return None


def get_target_channel_name_list():
    return ["halloween-poker", "ハロウィン・ポーカー" ]



# ２つのテキストの類似度の比較
def get_sequence_matcher_coef(test_1, text_2):

    # unicodedata.normalize() で全角英数字や半角カタカナなどを正規化する
    normalized_str1 = unicodedata.normalize('NFKC', test_1)
    normalized_str2 = unicodedata.normalize('NFKC', text_2)

    # 類似度を計算、0.0~1.0 で結果が返る
    s = difflib.SequenceMatcher(None, normalized_str1, normalized_str2).ratio()
    # print( "match ratio:" + str(s))
    return s



def get_ether_regist_channel(target_channel_obj):
    for ch in target_channel_obj.server.channels:
        if "イーサアドレス登録" in str(ch) or "eth-address" in str(ch) or "ethアドレス登録" in str(ch):
            return ch
            
    return None


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

GLOBAL_START_MESSAGE = None
GLOBAL_CLOSE_MESSAGE = None

GLOBAL_JACK_ACTING = False

GLOBAL_UNKO_JACK_MODE = {}
GLOBAL_UNKO_JACK_MODE["JACK"] = False

GLOBAL_REACTION_ICON_ROCK = False

# 前回実行した時間（時の部分だけ）
PRE_DATETIME_HOUR = -1

GLOBAL_REACTION_ICON = 0


GLOBAL_PLAYER = {}

# ログイン&準備が完了したら一度だけ実行される
@client.event
async def on_ready():

    global TRICK_OR_TREAT_CHANNEL
    global GLOBAL_START_MESSAGE
    global GLOBAL_CLOSE_MESSAGE
    global PRE_DATETIME_HOUR
    global GLOBAL_JACK_ACTING
    global GLOBAL_REACTION_ICON
    global GLOBAL_REACTION_ICON_ROCK

    # コンソールにBOTとしてログインした名前とUSER-IDを出力
    print('Logged in as')
    print('BOT-NAME :', client.user.name)
    print('BOT-ID   :', client.user.id)
    print('------')
    
    target_server_id = '443637824063930369' # BDA
    
    if "Test" in client.user.name:
        pass
        # target_server_id = '411022327380180992' # ★★★★★ こみやんま本舗でデバッグする時は、ここのコメントアウトをはずす
    
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

    cannel_bgm_cache = get_bgm_cache_channel(target_server_obj)

    # 起動時の時間をひかえる
    PRE_DATETIME_HOUR = datetime.datetime.now().hour
    print("時間" + str(PRE_DATETIME_HOUR))
    DATETIME_DAY = datetime.datetime.now().day
    print("日にち" + str(DATETIME_DAY))
    if target_server_obj:

        print("サーバー発見")
        while(True):
            target_channel_name = get_target_channel_name_list()
            
            nowdatetime = datetime.datetime.now()
            
            # 前回と同じ「時」であれば、次の「時」を待つ
            if PRE_DATETIME_HOUR == nowdatetime.hour:
                await asyncio.sleep(1)
                continue

            try:
                GLOBAL_REACTION_ICON = 0
                GLOBAL_JACK_ACTING = True
                GLOBAL_REACTION_ICON_ROCK = False
                print(target_channel_name)
                random_channel_name = random.choice(target_channel_name)
                target_channel_obj = None
                for c in target_server_obj.channels:
                    if c.name in target_channel_name:
                        target_channel_obj = c
                        
                
                if target_channel_obj:
                    
                    GLOBAL_START_MESSAGE = None
                    GLOBAL_CLOSE_MESSAGE = None
                    em = discord.Embed(title="", description="", color=0x36393f)
                    ret_message = await client.send_message(target_channel_obj, embed=em)

                    max_length = random.randint(1, 3)
                    if GLOBAL_UNKO_JACK_MODE["JACK"]:
                        max_length = 3
                        
                    jack_inner_mode = 0 # normal

                    if not GLOBAL_UNKO_JACK_MODE["JACK"]:
                        rand_jack = random.randint(1,7)
                        if rand_jack == 1:
                            jack_inner_mode = 1 #king mode
                        if rand_jack == 2:
                            jack_inner_mode = 2 #danbol mode
                        if rand_jack == 3:
                            jack_inner_mode = 3 #shampoo mode
                        if rand_jack == 4:
                            jack_inner_mode = 4 #kasa mode
                        if rand_jack == 5:
                            jack_inner_mode = 5 #chart mode
                        if rand_jack == 6:
                            jack_inner_mode = 6 #oden mode
                        if rand_jack == 7:
                            jack_inner_mode = 7 #toilet mode

                        if datetime.datetime.now().month == 10 and datetime.datetime.now().day == 31 and datetime.datetime.now().hour == 23:
                            jack_inner_mode = 98

                        if datetime.datetime.now().hour == 0 or datetime.datetime.now().hour == 24:
                            jack_inner_mode = 99

                    try:
                        if jack_inner_mode < 50:
                            await client.send_message(cannel_bgm_cache, "!halloween_poker_bgm_play gag_64k.mp3")
                        
                    except:
                        pass
                        
                    if jack_inner_mode == 0:
                        for r in range(0, max_length):
                            hmm_list = ["何だ...!? (What...!?)", "ふ～む...!? (Hmm...!?)", "どこだ...!? (Where...!?)", "甘い香り...!? (Sweet...!?)", "え～と...!? (Well...!?)", "う～む...!? (Um...!?)", "はは～ん...!? (Huh...!?)", "ふぁ...!? (No way...!?)", "なにごと...!? (Terrible...!?)", "ガスがあるのはココ...!? (Where Gass...!?)" ]
                            
                            if GLOBAL_UNKO_JACK_MODE["JACK"]:
                                if r == 0:
                                    hmm_list = [ "え、呼んだ...!?(Called...!?)" ] 
                                if r >= 2:
                                    hmm_list = [ "ガス不足...!? (gas shortage!?)" ]
                            
                            hmm = random.choice(hmm_list)
                            em.set_image(url=get_jack_o_lantern_to_r_direction(svr))
                            em.set_footer(text=hmm)
                            await client.edit_message(ret_message, embed=em)

                            await asyncio.sleep(5)

                            em.set_image(url=get_jack_o_lantern_to_l_direction(svr))
                            trc_list = ["何かもれちぁう...!? (Tr.c. o. .re.t!?)", "あ、でちゃう...? (Tr..k .r Tr.a.!?)", "うぇっぷ...!? (.ric. or ..eat!?)", "い...いく...!? (Tr.ck .. Tr.at!?)", "ガ...ガスが出る...!? (Tr.ck .. Tr.at!?)" ]
                            if r == max_length-1:
                                trc_list = ["も! もれちゃうーー!! (Daammnn---!!)", "あー! でちゃうー!! (Aiieee---!!)", "うっぷーー あ!! (Yiiipee---!!)", "い、いくーーー!! (Eeeekk---!!)", "あたま屁ガスーー!! (Faaarrt---!!)", ]
                            if GLOBAL_UNKO_JACK_MODE["JACK"]:
                                if r == 1:
                                    trc_list = ["メタンガス持ち...?? (I've methane gas...??)" ]
                                else:
                                    trc_list = ["頭のうえ...?? (Head on top...!?)" ]
                                if r == max_length-1:
                                    trc_list = ["ガスがあふれるーー!! (Gas overflows---!!)" ]

                            trc = random.choice(trc_list)

                            em.set_footer(text=trc)
                            await client.edit_message(ret_message, embed=em)

                            await asyncio.sleep(5)

                            # 念のため消しておく
                            GLOBAL_REACTION_ICON = 0
                            
                        # 念のため消しておく
                        GLOBAL_REACTION_ICON = 0
                            
                    # 王冠モード
                    elif jack_inner_mode == 1:
                        em.set_image(url=get_jack_o_lantern_to_r_direction(svr))
                        em.set_footer(text="いいもんめっけたw (I found something good!, lol.)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                        em.set_footer(text="じゃじゃーん!! 王冠!! (Well Shazam!! Crown!!)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_r_direction(svr, jack_inner_mode))
                        em.set_footer(text="キングww (I'm a King, lol)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                        em.set_footer(text="...ふぁ!? (...What!?)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_r_direction(svr, jack_inner_mode))
                        em.set_footer(text="...外れない!? (...Not come off!?)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                        em.set_footer(text="...誰か👑引っ張って!! (...Pulling 👑!!)")
                        await client.edit_message(ret_message, embed=em)
                        #await client.add_reaction(ret_message, ":point_right::skin-tone-2:")
                        #emjs = client.get_all_emojis()
                        #print(emjs)
                        GLOBAL_REACTION_ICON = 0
                        await client.add_reaction(ret_message, "👉")
                        await client.add_reaction(ret_message, "👑")
                        await client.add_reaction(ret_message, "👈")
                        
                        for k in range(0, 5):
                            if GLOBAL_REACTION_ICON > 60:
                                em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                                em.set_footer(text="...そんなに引っ張っちゃ らめー!! (...Do not pull me so much!!)")
                                await client.edit_message(ret_message, embed=em)
                                break
                            elif k==4:
                                em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                                em.set_footer(text="...んにに!! とれるーー!! (...Mnn!! Come off!!)")
                                await client.edit_message(ret_message, embed=em)
                                break
                            elif GLOBAL_REACTION_ICON >= 35:
                                em.set_image(url=get_jack_o_lantern_to_r_direction(svr, jack_inner_mode))
                                em.set_footer(text="...その調子ーー!! (...you're doing great!!)")
                                await client.edit_message(ret_message, embed=em)
                                await asyncio.sleep(5)
                            else:
                                await asyncio.sleep(5)

                        await asyncio.sleep(5)

                    # 段ボールモード
                    elif jack_inner_mode == 2:
                        em.set_image(url=get_jack_o_lantern_to_close(svr, jack_inner_mode))
                        em.set_footer(text="...💤")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_r_direction(svr, jack_inner_mode))
                        em.set_footer(text="...ん? (Hmm?)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                        em.set_footer(text="...時間!?... (...It's time!?)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_r_direction(svr, jack_inner_mode))
                        em.set_footer(text="...ここワシんち (...This is my house)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                        em.set_footer(text="...産地直送!? (...Farm-fresh!?)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_close(svr, jack_inner_mode))
                        em.set_footer(text="...じゃ、また... (See u later...)")
                        await client.edit_message(ret_message, embed=em)
                        
                        GLOBAL_REACTION_ICON = 0
                        await client.add_reaction(ret_message, "👉")
                        await client.add_reaction(ret_message, "📦")
                        await client.add_reaction(ret_message, "👈")

                        for k in range(0, 5):
                            if GLOBAL_REACTION_ICON > 60:
                                em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                                em.set_footer(text="...えーい!! 眠れんわーい!! (...Eh! clamorous!! I can't sleep!!)")
                                await client.edit_message(ret_message, embed=em)
                                break
                            elif k==4:
                                em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                                em.set_footer(text="...はよ起こさんかーい!! (...Wake me up!!)")
                                await client.edit_message(ret_message, embed=em)
                                break
                            elif GLOBAL_REACTION_ICON >= 35:
                                em.set_image(url=get_jack_o_lantern_to_close(svr, jack_inner_mode))
                                em.set_footer(text="...う、うーん💢 (...Um..Ummm 💢)")
                                await client.edit_message(ret_message, embed=em)
                                await asyncio.sleep(5)
                            else:
                                await asyncio.sleep(5)

                        await asyncio.sleep(5)



                    # シャンプハットモード
                    elif jack_inner_mode == 3:
                        em.set_image(url=get_jack_o_lantern_to_r_direction(svr, jack_inner_mode))
                        em.set_footer(text="ふ～んふん❤ (uh-huh❤)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(3)

                        em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                        em.set_footer(text="🎶張っつくパンツか🎶 (ha!! tu! ku! pa! nn! tu! ka!🎶)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(2.5)
                        em.set_image(url=get_jack_o_lantern_to_r_direction(svr, jack_inner_mode))
                        em.set_footer(text="🎶引っ付くパンツか🎶 (hi!! tu! ku! pa! nn! tu! ka!🎶)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(2.5)

                        em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                        em.set_footer(text="🎶くっつくパンツか🎶 (ku!! tu! ku! pa! nn! tu! ka!🎶)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(2.5)

                        em.set_image(url=get_jack_o_lantern_to_r_direction(svr, jack_inner_mode))
                        em.set_footer(text="🎶もっこりパンツか🎶 (mo!! ko! ri! pa! nn! tu! ka!🎶)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(2.5)

                        em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                        em.set_footer(text="🎶ボイパ イェーぃ🎶 (Yeh!!)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(3)

                        em.set_image(url=get_jack_o_lantern_to_r_direction(svr, jack_inner_mode))
                        em.set_footer(text="...パンツじゃなくスカート!?... (...not pants but skirt!?)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(4)

                        em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                        em.set_footer(text="...これはシャンプーハット❤ (This is a Shampoo Hat❤)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(4)

                        em.set_image(url=get_jack_o_lantern_to_r_direction(svr, jack_inner_mode))
                        em.set_footer(text="...あれ？ シャワーは!? (...What!? Where's a Shower!?)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(4)

                        em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                        em.set_footer(text="...ちょ!! だれかシャワーよろ! (Hey! Please bring a Shower!)")
                        await client.edit_message(ret_message, embed=em)
                        
                        GLOBAL_REACTION_ICON = 0
                        await client.add_reaction(ret_message, "👉")
                        await client.add_reaction(ret_message, "🚿")
                        await client.add_reaction(ret_message, "👈")

                        for k in range(0, 5):
                            if GLOBAL_REACTION_ICON > 60:
                                em.set_image(url=get_jack_o_lantern_to_l_direction_shower(svr, jack_inner_mode))
                                em.set_footer(text="...あ!! ちょ!! あっちーー!! (...Ah!! Too HOOOOOOT!!)")
                                await client.edit_message(ret_message, embed=em)
                                break
                            elif GLOBAL_REACTION_ICON >= 30:
                                if k % 2 == 0:
                                    em.set_image(url=get_jack_o_lantern_to_r_direction_shower(svr, jack_inner_mode))
                                else:
                                    em.set_image(url=get_jack_o_lantern_to_l_direction_shower(svr, jack_inner_mode))
                                    
                                em.set_footer(text="...あー、いい感じ❤ (...Oh Good❤)")
                                await client.edit_message(ret_message, embed=em)
                                await asyncio.sleep(5)
                            elif GLOBAL_REACTION_ICON < 30:
                                await asyncio.sleep(5)
                                if k % 2 == 0:
                                    em.set_image(url=get_jack_o_lantern_to_r_direction(svr, jack_inner_mode))
                                else:
                                    em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                                    
                                em.set_footer(text="...ちょ!! だれかシャワーよろ!! (Hey! please bring a Shower!!)")
                                await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)


                    # 傘
                    elif jack_inner_mode == 4:
                        em.set_image(url=get_jack_o_lantern_to_r_direction(svr))
                        em.set_footer(text="いいもんめっけたw (I found something good!, lol.)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_l_direction_kasa(svr, jack_inner_mode, "orange"))
                        em.set_footer(text="じゃじゃーん!! かさ!! (Well Shazam!! Umbrella!!)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_r_direction_kasa(svr, jack_inner_mode, "orange"))
                        em.set_footer(text="カボチャ付きww (The Pumpkin is on this, lol)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_l_direction_kasa(svr, jack_inner_mode, "orange"))
                        em.set_footer(text="せーの!! (Ready!!) ")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(4)
                        em.set_image(url=get_jack_o_lantern_to_l_direction_kasa(svr, jack_inner_mode, "orange_up"))
                        em.set_footer(text="よっしょい～!! (Go!!) ")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(4)

                        em.set_image(url=get_jack_o_lantern_to_r_direction_kasa(svr, jack_inner_mode, "orange"))
                        em.set_footer(text="ほいっと～!! (Catch!!) ")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(4)

                        em.set_image(url=get_jack_o_lantern_to_r_direction_kasa(svr, jack_inner_mode, "orange_kaze"))
                        em.set_footer(text="ふあ!? 風が!! (...What!? Wind!!?)")
                        await client.edit_message(ret_message, embed=em)
                        
                        await asyncio.sleep(4)

                        em.set_image(url=get_jack_o_lantern_to_l_direction_kasa(svr, jack_inner_mode, "orange_kaze"))
                        em.set_footer(text="浮いちゃう!! 誰か助けて!! (I'm floating!! Help me!!)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(4)
                        
                        GLOBAL_REACTION_ICON = 0
                        await client.add_reaction(ret_message, "👉")
                        await client.add_reaction(ret_message, "🎃")
                        await client.add_reaction(ret_message, "👈")

                        for k in range(0, 5):
                            if GLOBAL_REACTION_ICON > 60:
                                em.set_image(url=get_jack_o_lantern_to_l_direction_kasa(svr, jack_inner_mode, "orange_kaze"))
                                em.set_footer(text="...そんなに引っ張っちゃ らめー!! (...Do not pull me so much!!)")
                                await client.edit_message(ret_message, embed=em)
                                break
                            elif k==4:
                                em.set_image(url=get_jack_o_lantern_to_l_direction_kasa(svr, jack_inner_mode, "orange_kaze"))
                                em.set_footer(text="...ああー 体がもっていかれるー!! (...Oh!! My body floats in the air!!)")
                                await client.edit_message(ret_message, embed=em)
                                break
                            elif GLOBAL_REACTION_ICON >= 35:
                                if k % 2 == 0:
                                    em.set_image(url=get_jack_o_lantern_to_r_direction_kasa(svr, jack_inner_mode, "orange_kaze"))
                                else:
                                    em.set_image(url=get_jack_o_lantern_to_l_direction_kasa(svr, jack_inner_mode, "orange_kaze"))
                                em.set_footer(text="...その調子ーー!! (...you're doing great!!)")
                                await client.edit_message(ret_message, embed=em)
                                await asyncio.sleep(5)
                            else:
                                if k % 2 == 0:
                                    em.set_image(url=get_jack_o_lantern_to_l_direction_kasa(svr, jack_inner_mode, "orange_kaze"))
                                else:
                                    em.set_image(url=get_jack_o_lantern_to_l_direction_kasa(svr, jack_inner_mode, "orange_kaze"))
                                em.set_footer(text="浮いちゃう!! 誰か助けて!! (I'm floating!! Help me!!)")
                                await client.edit_message(ret_message, embed=em)
                                await asyncio.sleep(5)

                        await asyncio.sleep(5)



                    # チャート
                    elif jack_inner_mode == 5:

                        em.set_image(url=get_jack_o_lantern_to_chart(svr, jack_inner_mode, "1st"))
                        em.set_footer(text="さてコインの相場は... (Well then, Crypto Market price)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_chart(svr, jack_inner_mode, "2nd"))
                        em.set_footer(text="あがってるー!! (It's going up!!)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_chart(svr, jack_inner_mode, "3rd"))
                        em.set_footer(text="一気にくるーっと!? ふぁ!? (Stretch!! Go!! Rotate!! What!?")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_chart(svr, jack_inner_mode, "4th"))
                        em.set_footer(text="ふぁー😱!? 床を砕いたーー!!? (It crushes the floor!!?)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(6)

                        em.set_image(url=get_jack_o_lantern_to_chart(svr, jack_inner_mode, "5th"))
                        em.set_footer(text="ふぁ😲!?")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(3)

                        em.set_image(url=get_jack_o_lantern_to_chart(svr, jack_inner_mode, "5th"))
                        em.set_footer(text="上がれ～～～んぎぎぎ!!! (Riiiiise!!! Cooooome!!!)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(4)
                        
                        GLOBAL_REACTION_ICON = 0
                        await client.add_reaction(ret_message, "👉")
                        await client.add_reaction(ret_message, "📈")
                        await client.add_reaction(ret_message, "👈")

                        for k in range(0, 5):
                            if GLOBAL_REACTION_ICON > 60:
                                em.set_image(url=get_jack_o_lantern_to_chart(svr, jack_inner_mode, "6th"))
                                em.set_footer(text="パンプキン!!! ムーーーン!! (Pumpkin!! Mooooooonn!!)")
                                await client.edit_message(ret_message, embed=em)
                                break
                            elif k==4:
                                em.set_image(url=get_jack_o_lantern_to_chart(svr, jack_inner_mode, "6th"))
                                em.set_footer(text="なんとか ムーーーン!! (barely! Mooooooonn!)")
                                await client.edit_message(ret_message, embed=em)
                                break
                            elif GLOBAL_REACTION_ICON >= 35:
                                if k % 2 == 0:
                                    em.set_footer(text="...その調子ーー!! (...you're doing great!!)")
                                else:
                                    em.set_footer(text="...いいよいいよーー!! (...you're doing very nice!!)")
                                await client.edit_message(ret_message, embed=em)
                                await asyncio.sleep(5)
                            else:
                                if k % 2 == 0:
                                    em.set_footer(text="...負けるな～～～んごごご!!! (...Riiiiise!!! Gooooooo!!!)")
                                else:
                                    em.set_footer(text="...上がれ～～～んぎぎぎ!!! (...Riiiiise!!! Cooooome!!!)")
                                await client.edit_message(ret_message, embed=em)
                                await asyncio.sleep(5)

                        await asyncio.sleep(5)

                    # おでんモード
                    elif jack_inner_mode == 6:
                        em.set_image(url=get_jack_o_lantern_to_r_direction(svr, jack_inner_mode))
                        em.set_footer(text="...シー! (Shhhh!)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                        em.set_footer(text="...いま覆面で潜入調査中! (...I'm under sneak survey, now!)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_r_direction(svr, jack_inner_mode))
                        em.set_footer(text="ここ!? (Here?)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                        em.set_footer(text="...ローソンのおでんケースの中w (...In Oden Box of Lawson's , lol)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_r_direction(svr, jack_inner_mode))
                        em.set_footer(text="...さて、帰るかな! (...Well, I will return home!)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                        em.set_footer(text="...あれ？ 外れない!! (What!? ...Not come off!!)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_r_direction(svr, jack_inner_mode))
                        em.set_footer(text="...誰か🍢引っ張って!! (...Pulling 🍢!!)")
                        await client.edit_message(ret_message, embed=em)

                        GLOBAL_REACTION_ICON = 0
                        await client.add_reaction(ret_message, "👉")
                        await client.add_reaction(ret_message, "🍢")
                        await client.add_reaction(ret_message, "👈")

                        await asyncio.sleep(5)
                        
                        for k in range(0, 5):
                            if GLOBAL_REACTION_ICON > 60:
                                em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                                em.set_footer(text="...そんなにこんにゃく引っ張っちゃ らめー!! (...Do not pull the Konjac so much!!)")
                                await client.edit_message(ret_message, embed=em)
                                break
                            elif k==4:
                                em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                                em.set_footer(text="...んにに!! ぬけるーー!! (...Mnn!! Come off!!)")
                                await client.edit_message(ret_message, embed=em)
                                break
                            elif GLOBAL_REACTION_ICON >= 35:
                                if k % 2 == 0:
                                    em.set_footer(text="...その調子ーー!! (...you're doing great!!)")
                                    em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                                else:
                                    em.set_footer(text="...いいよいいよーー!! (...you're doing very nice!!)")
                                    em.set_image(url=get_jack_o_lantern_to_r_direction(svr, jack_inner_mode))
                                await client.edit_message(ret_message, embed=em)
                                await asyncio.sleep(5)
                            else:
                                if k % 2 == 0:
                                    em.set_footer(text="...身バレしちゃう💔 (...My Background will be revealed💔)")
                                    em.set_image(url=get_jack_o_lantern_to_l_direction(svr, jack_inner_mode))
                                else:
                                    em.set_footer(text="...誰か🍢引っ張って!! (...Pulling 🍢!!)")
                                    em.set_image(url=get_jack_o_lantern_to_r_direction(svr, jack_inner_mode))
                                await client.edit_message(ret_message, embed=em)
                                await asyncio.sleep(5)

                        await asyncio.sleep(5)


                    # トイレ
                    elif jack_inner_mode == 7:

                        em.set_image(url=get_jack_o_lantern_to_close(svr, jack_inner_mode))
                        em.set_footer(text="...")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(4)

                        em.set_image(url=get_jack_o_lantern_to_toilet(svr, jack_inner_mode, "1st"))
                        em.set_footer(text="...")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(3)

                        em.set_footer(text="...やぁ (...Hello)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(3)


                        em.set_footer(text="ここワープゲートw (Here is a warp gate, lol)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_footer(text="今、故障してるみたいw (It seems to be broken now, lol)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.set_footer(text="ちょこっとぬいて❤ (Pull me a little❤)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)
                        
                        GLOBAL_REACTION_ICON = 0
                        await client.add_reaction(ret_message, "👉")
                        await client.add_reaction(ret_message, "🚽")
                        await client.add_reaction(ret_message, "🎃")
                        await client.add_reaction(ret_message, "👈")

                        for k in range(0, 5):
                            if GLOBAL_REACTION_ICON > 60:
                                em.set_footer(text="やっと抜けたー!! (Yes!! I'm free!!))")
                                em.set_image(url=get_jack_o_lantern_to_toilet(svr, jack_inner_mode, "3rd"))
                                await client.edit_message(ret_message, embed=em)

                                await asyncio.sleep(4)

                                em.set_footer(text="ックショ!!! (achoo!!!))")
                                await client.edit_message(ret_message, embed=em)
                                break
                            elif k==4:
                                em.set_footer(text="あ、抜けた! (Oh, Success!)")
                                em.set_image(url=get_jack_o_lantern_to_toilet(svr, jack_inner_mode, "3rd"))
                                await client.edit_message(ret_message, embed=em)

                                await asyncio.sleep(4)

                                em.set_footer(text="ックショ!!! (achoo!!!))")
                                await client.edit_message(ret_message, embed=em)
                                break
                            elif GLOBAL_REACTION_ICON >= 35:
                                if k % 2 == 0:
                                    em.set_footer(text="...その調子ーー!! (...you're doing great!!)")
                                else:
                                    em.set_footer(text="...いいよいいよーー!! (...you're doing very nice!!)")
                                em.set_image(url=get_jack_o_lantern_to_toilet(svr, jack_inner_mode, "2nd"))
                                await client.edit_message(ret_message, embed=em)
                                await asyncio.sleep(5)
                            else:
                                if k % 2 == 0:
                                    em.set_footer(text="...あ、水が入ってきた🚽 (...Oh, the water came in🚽)")
                                else:
                                    em.set_footer(text="ちょこっとぬいて❤ (Pull me a little❤)")
                                await client.edit_message(ret_message, embed=em)
                                await asyncio.sleep(5)

                            await asyncio.sleep(3)

                    # 闇の登場
                    elif jack_inner_mode == 98:
                        em.set_footer(text="この劇はかなり長くなっています。メニューの「ハロウィン・ＢＧＭ」への接続がお勧めです。")
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(8)

                        em1 = discord.Embed(title="", description="", color=0x36393f)
                        em1.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "1st"))
                        em1.set_footer(text="ブラックだわ！")
                        ecmsg1 = await client.send_message(target_channel_obj, embed=em1)
                        await asyncio.sleep(2)

                        em2 = discord.Embed(title="", description="", color=0x36393f)
                        em2.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "2nd"))
                        em2.set_footer(text="逃げろ！")
                        ecmsg2 = await client.send_message(target_channel_obj, embed=em2)
                        await asyncio.sleep(2)

                        em3 = discord.Embed(title="", description="", color=0x36393f)
                        em3.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "3rd"))
                        em3.set_footer(text="スイーツないかしら💛")
                        ecmsg3 = await client.send_message(target_channel_obj, embed=em3)
                        await asyncio.sleep(1)
                        await client.delete_message(ecmsg1)
                        await asyncio.sleep(1)

                        em4 = discord.Embed(title="", description="", color=0x36393f)
                        em4.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "4th"))
                        em4.set_footer(text="やつが来た！")
                        ecmsg4 = await client.send_message(target_channel_obj, embed=em4)
                        await asyncio.sleep(1)
                        await client.delete_message(ecmsg2)
                        await asyncio.sleep(1)

                        em5 = discord.Embed(title="", description="", color=0x36393f)
                        em5.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "5th"))
                        em5.set_footer(text="隠れろ！")
                        ecmsg5 = await client.send_message(target_channel_obj, embed=em5)
                        await asyncio.sleep(1)
                        await client.delete_message(ecmsg3)

                        await asyncio.sleep(1)

                        em6 = discord.Embed(title="", description="", color=0x36393f)
                        em6.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "6th"))
                        em6.set_footer(text="ヤミじゃ! 早く逃げるんじゃ！\n")
                        ecmsg6 = await client.send_message(target_channel_obj, embed=em6)

                        await asyncio.sleep(1)
                        await client.delete_message(ecmsg4)
                        await asyncio.sleep(1)
                        await client.delete_message(ecmsg5)
                        await asyncio.sleep(1)

                        await client.delete_message(ecmsg6)

                        await client.send_message(cannel_bgm_cache, "!halloween_poker_bgm_play devil_battle_64k.mp3")
                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "7th"))
                        em.set_footer(text="(パタパタパタ…)")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(16)
                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "8th"))
                        em.set_footer(text="(ぶっほっほっほ)", icon_url=get_boss_icon(svr) )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(8)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "9th"))
                        em.set_footer(text="(ここか、次なるエサ場は… ぐっふっふ)", icon_url=get_boss_icon(svr) )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "10th"))
                        em.set_footer(text="...？", icon_url=get_boss_icon(svr) )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(3)

                        jack_avator_url = client.user.avatar_url.replace(".webp?", ".png?")

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "11th"))
                        em.set_footer(text="ねぇ、あんたボス...？", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "11th"))
                        em.set_footer(text="え？ あ、はい。ブラックボスです...", icon_url=get_boss_icon(svr) )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "12th"))
                        em.set_footer(text="あっそ。ちょっとそこで待っといて～", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(4)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "25th"))
                        em.set_footer(text="あっ...", icon_url=get_boss_icon(svr) )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(4)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "9th"))
                        em.set_footer(text="はい...", icon_url=get_boss_icon(svr) )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(4)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "9th"))
                        em.set_footer(text="一体何者...？", icon_url=get_boss_icon(svr) )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "13th"))
                        em.set_footer(text="メンドクサイのぅ～", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "14th"))
                        em.set_footer(text="あれやるかのぅ～", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "15th"))
                        em.set_footer(text="このダンボールは「契約の箱」。", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_footer(text="すごい箱。", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "16th"))
                        em.set_footer(text="このおでんの棒を", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "15th"))
                        em.set_footer(text="入れると...", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "17th"))
                        em.set_footer(text="おでんの棒 ⇒ オーディンの槍に！", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "18th"))
                        em.set_footer(text="顔がついた傘を", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "15th"))
                        em.set_footer(text="入れると...", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "19th"))
                        em.set_footer(text="イージスの盾に！", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "20th"))
                        em.set_footer(text="王冠とシャンプーハットを", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "15th"))
                        em.set_footer(text="入れると...", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "21th"))
                        em.set_footer(text="大天使のカブトに！", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "14th"))
                        em.set_footer(text="時間ないので 巻きで！", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "23th"))
                        em.set_footer(text="じゃじゃーん！ 真の姿！", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "26th"))
                        em.set_footer(text="我こそ、勇者･ダイヤモンド･エース!!(I'm Brave Diamond Ace!!)", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "27th"))
                        em.set_footer(text="やはり 天の使いであったかーー!", icon_url=get_boss_icon(svr) )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(4)

                        em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "8th"))
                        em.set_footer(text="バカナーー!!!! ギャァァぁーーーー!!!!", icon_url=get_boss_icon(svr) )
                        await client.edit_message(ret_message, embed=em)

                        GLOBAL_REACTION_ICON = 300
                        await client.add_reaction(ret_message, "👉")
                        await client.add_reaction(ret_message, "🦇")
                        await client.add_reaction(ret_message, "👈")

                        await asyncio.sleep(4)

                        em1.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "7st"))
                        em.set_footer(text="(パタパタパタ…)", icon_url=get_boss_icon(svr) )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(4)
                        

                    # 闇の登場
                    elif jack_inner_mode == 99:
                        em.set_footer(text="エンディングとなります。メニューの「ハロウィン・ＢＧＭ」への接続がお勧めです。")
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(20)

                        jack_avator_url = client.user.avatar_url.replace(".webp?", ".png?")

                        await client.send_message(cannel_bgm_cache, "!halloween_poker_bgm_play ending_64k.mp3")

                        await asyncio.sleep(1)
                        em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "2nd"))
                        em.set_footer(text="🎧ふふふ～ん🎧", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "1st"))
                        em.set_footer(text="🎧ほほほ～ん🎧", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "2nd"))
                        em.set_footer(text="〔❔ 謎の声：...あーあー テストテスト...  エース、聞こえる？〕")
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "1st"))
                        em.set_footer(text="ふぁ!?", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(4)

                        em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "2nd"))
                        em.set_footer(text="〔❔ 謎の声：...ゲートが直ったから帰っておいでー〕")
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "1st"))
                        em.set_footer(text="お!? マジ!?", icon_url=jack_avator_url )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(4)

                        em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "3rd"))
                        em.set_footer(text="じゃ、帰るかな～" )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "4th"))
                        em.set_footer(text="..." )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(4)

                        em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "5th"))
                        em.set_footer(text="色んなことがあったな～" )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "6th"))
                        em.set_footer(text="またきっと会えるさ～" )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(4)

                        em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "7th"))
                        em.set_footer(text="それじゃいくね..." )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "8th"))
                        em.set_footer(text="あ、それお守りな!" )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "9th"))
                        em.set_footer(text="そんじゃいくわ..." )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)

                        em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "10th"))
                        em.set_footer(text="..." )
                        await client.edit_message(ret_message, embed=em)
                        await asyncio.sleep(5)
                        
                        em.clear_fields()
                        em.set_footer(text=" " )
                        em.add_field(name="🎃 提供 🎃", value="BLACKDIA LLC\n**　**\n", inline=False)
                        em.add_field(name="🎃 制作 🎃", value="こみやんま\n**　**\n", inline=False)
                        em.add_field(name="🎃 ＢＧＭ 🎃", value="ユーフルカ　Golmont\n**　**\n", inline=False)
                        # em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "toumei"))
                        em.set_image(url="")
                        await client.edit_message(ret_message, embed=em)
                        
                        result_channel = get_poker_result_channel(svr)
                        await client.send_message(result_channel, embed=em)
                        
                        await asyncio.sleep(7)
                        
                        await ending_scroll_sanka(svr, ret_message, em, target_channel_obj)

                        em.clear_fields()
                        
                        em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "toumei"))
                        em.set_footer(text="")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(3)

                        em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "toumei"))
                        em.set_footer(text="─ その後、ジャック･オー･ランターン ...")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(4)

                        em.clear_fields()
                        em.set_footer(text="Brave･Diamond･Ace の姿を見たものは、いない。")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)


                        em.clear_fields()
                        em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "12th"))
                        em.set_footer(text="だが、彼が居たことを後の世に伝えるため")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.clear_fields()
                        em.set_footer(text="私はここにこの物語を残そう・・・")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.clear_fields()
                        # em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "12th"))
                        em.set_footer(text="ハロウィン・ポーカー・ストーリー 著者")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(5)

                        em.clear_fields()
                        # em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "12th"))
                        em.set_footer(text="コミヤンマ・アークティ・グヌーン")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(6)

                        em.clear_fields()
                        em.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "fin_full"))
                        em.set_footer(text="")
                        await client.edit_message(ret_message, embed=em)

                        await asyncio.sleep(20)

                        em3 = discord.Embed(title="", description="", color=0x36393f)
                        em3.set_image(url=get_jack_o_lantern_to_ending(svr, jack_inner_mode, "coin"))
                        em3.add_field(name="Brave Diamond Ace のコイン", value= "JACKがお守りとして残したコイン", inline=False)
                        em3.set_footer(text="JACKの名前と姿が彫られている...")
                        await client.send_message(target_channel_obj, embed=em3)
                        await client.send_message(result_channel, embed=em3)
                        


                    # BGMの停止
                    try:
                        await client.send_message(cannel_bgm_cache, "!halloween_poker_bgm_fadeout")
                    except:
                        pass

                    

                    if random.random() < 1.1 and jack_inner_mode < 99: # ★ 0.6 などとすると帰ることがある★
                    
                        PRE_DATETIME_HOUR = nowdatetime.hour

                        if jack_inner_mode == 98:
                            em.set_image(url=get_jack_o_lantern_to_yamitojo(svr, jack_inner_mode, "7th"))
                        else:
                            em.set_image(url=get_jack_o_lantern_trick_or_treat(svr, jack_inner_mode))
                        em.set_footer(text=" ")
                        await client.edit_message(ret_message, embed=em)

                        TRICK_OR_TREAT_CHANNEL = target_channel_obj
                        # 万が一のときんためにtryしておく
                        try:
                            GLOBAL_REACTION_ICON_ROCK = True
                            
                            g_start_message = None
                            
                            if jack_inner_mode == 98:
                                g_start_message = await client.send_message(target_channel_obj, " :bat: :regional_indicator_b: :regional_indicator_l: :regional_indicator_a: :regional_indicator_c: :regional_indicator_k: :bat:")
                            else:
                                # HAPPY
                                g_start_message = await client.send_message(target_channel_obj, " :tada: :regional_indicator_h: :regional_indicator_a: :regional_indicator_p: :regional_indicator_p: :regional_indicator_y: :tada:")
                            
                            GLOBAL_START_MESSAGE = g_start_message.id
                            await asyncio.sleep(30)
                            
                            ghost_message = await client.send_message(target_channel_obj, "…")
                            await asyncio.sleep(0.5)
                            await client.edit_message(ghost_message, ":ghost:…………………………………………")
                            await asyncio.sleep(0.5)
                            await client.edit_message(ghost_message, "…………:ghost:………………………………")
                            await asyncio.sleep(0.5)
                            await client.edit_message(ghost_message, "……………………:ghost:……………………")
                            await asyncio.sleep(0.5)
                            await client.edit_message(ghost_message, "………………………………:ghost:…………")
                            await asyncio.sleep(0.5)
                            await client.edit_message(ghost_message, "…………………………………………:ghost:")
                            await asyncio.sleep(1)
                            await client.delete_message(ghost_message)
                            await asyncio.sleep(6)

                            g_close_message = None
                            if jack_inner_mode == 98:
                                # CLOSE
                                g_close_message = await client.send_message(target_channel_obj, ":bat: :regional_indicator_c: :regional_indicator_l: :regional_indicator_o: :regional_indicator_s: :regional_indicator_e: :bat:")
                            
                            else:
                                # CLOSE
                                g_close_message = await client.send_message(target_channel_obj, ":jack_o_lantern: :regional_indicator_c: :regional_indicator_l: :regional_indicator_o: :regional_indicator_s: :regional_indicator_e: :jack_o_lantern:")
                            GLOBAL_CLOSE_MESSAGE = g_close_message.id
                            TRICK_OR_TREAT_CHANNEL = None
                            
                            print(TRICK_OR_TREAT_TIME_POKER_REGIST_LIST)

                            if len(TRICK_OR_TREAT_TIME_POKER_REGIST_LIST) > 0:

                                # キーと値のうち、値の方のpointでソート。
                                sorted_list = sorted(TRICK_OR_TREAT_TIME_POKER_REGIST_LIST.items(), key=lambda x: x[1]["point"], reverse=True )
                                # print("★"+str(sorted_list))

                                ranchange_amaount = 1000000000
                                medal_str_list = ["", ":first_place:",":second_place:",":third_place:",":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:",":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:", ":medal:"]

                                index_list_ix = 0
                                
                                poop = 0
                                
                                result_str_list = []
                                result_str_list.append("─ **今回**の結果 ─\n　(The result of **this** time)\n\n")
                                
                                for s in sorted_list:
                                    index_list_ix = index_list_ix + 1
                                    if len(sorted_list) >=10:
                                        number_padding = "{0:02d}".format(index_list_ix)
                                    else:
                                        number_padding = str(index_list_ix)
                                        
                                    medal = ""
                                    if s[1]["point"] < 100:
                                        medal = ":pig:"
                                        # 最後の要素でかつ、
                                        if s is sorted_list[-1] and s[1]["point"] < ranchange_amaount:
                                            medal = ":poop:"
                                            # パンプキンが入っている
                                            if "9D" in TRICK_OR_TREAT_TIME_POKER_REGIST_LIST[ s[0] ]["bests"]:
                                                poop = s[0]
                                        ranchange_amaount = s[1]["point"]

                                    elif s[1]["point"] == 100:
                                        medal = ":dog:"
                                        ranchange_amaount = s[1]["point"]

                                    # 報酬が同じなら、同じなら今先頭にあるメダルをそのまま使う
                                    elif s[1]["point"] == ranchange_amaount:
                                        medal = medal_str_list[0]
                                    
                                    elif s[1]["point"] < ranchange_amaount:
                                        medal_str_list.pop(0)
                                        medal = medal_str_list[0]
                                        ranchange_amaount = s[1]["point"]
                                        
                                    result_str_list.append(number_padding + ". " + medal + " <@" + str(s[0]) + ">" + "      " + str(s[1]["point"]) + " BDA Get!!\n")
                                    if index_list_ix >= 65:
                                        # その他にいたら略する
                                        if len(sorted_list) > 65:
                                            result_str_list.append("...その他(Others) " + str(len(sorted_list)-index_list_ix) + " 人\n")

                                        break

                                try:
                                    await client.send_message(target_channel_obj, ".\n")
                                    await asyncio.sleep(0.2)
                                except:
                                    pass

                                result_string = ""
                                for line_ix in range(0, len(result_str_list)):
                                    line_str = result_str_list[line_ix]
                                    result_string = result_string + line_str
                                    
                                    # ％で割った最後の値か、もしくは配列の長さの最後の値
                                    if line_ix % 30 == 29 or line_ix == len(result_str_list)-1:
                                        try:
                                            result_aaa = await client.send_message(target_channel_obj, result_string)
                                            await asyncio.sleep(0.5)
                                        except:
                                            result_aaa = None
                                        
                                        if result_aaa == None:
                                            await asyncio.sleep(0.5)
                                            try:
                                                result_aaa = await client.send_message(target_channel_obj, result_string)
                                            except:
                                                result_aaa = None

                                        if result_aaa == None:
                                            await asyncio.sleep(0.5)
                                            try:
                                                result_aaa = await client.send_message(target_channel_obj, result_string)
                                            except:
                                                result_aaa = None
                                                
                                        result_string = ""

                                try:
                                    await client.send_message(target_channel_obj, ".\n")
                                    await asyncio.sleep(0.2)
                                except:
                                    pass

                                result_all_message, em_poop = await calc_of_all_poker(target_channel_obj, TRICK_OR_TREAT_TIME_POKER_REGIST_LIST, poop)
                                if result_all_message != "":
                                    await client.send_message(target_channel_obj, str(result_all_message))
                                else:
                                    await client.send_message(target_channel_obj, "総計が空っぽ")

                                if em_poop:
                                    await asyncio.sleep(10)
                                    await client.send_message(target_channel_obj, embed=em_poop)

                        except Exception as e4:
                            TRICK_OR_TREAT_CHANNEL = None

                            t, v, tb = sys.exc_info()
                            print(traceback.format_exception(t,v,tb))
                            print(traceback.format_tb(e4.__traceback__))

                            # CLOSE
                            await client.send_message(target_channel_obj, ":jack_o_lantern: :regional_indicator_c: :regional_indicator_l: :regional_indicator_o: :regional_indicator_s: :regional_indicator_e: :jack_o_lantern:")
                            
                    else:
                        PRE_DATETIME_HOUR = nowdatetime.hour
                        await asyncio.sleep(5000)
                        GLOBAL_REACTION_ICON_ROCK = False

                        TRICK_OR_TREAT_CHANNEL = None
                        
                print("スリープ")
                await asyncio.sleep(3)
                await client.send_message(cannel_bgm_cache, "!halloween_poker_bgm_stop")
                await asyncio.sleep(27)
                GLOBAL_REACTION_ICON = 0
                GLOBAL_REACTION_ICON_ROCK = False
                TRICK_OR_TREAT_TIME_POKER_REGIST_LIST.clear()
                print("GLOBAL_UNKO_JACK_MODE Falseに代入")
                GLOBAL_UNKO_JACK_MODE["JACK"] = False
                GLOBAL_JACK_ACTING = False
            except Exception as e2:
                t, v, tb = sys.exc_info()
                print(traceback.format_exception(t,v,tb))
                print(traceback.format_tb(e2.__traceback__))
                print("例外:poker hand_percenteges error")
                await asyncio.sleep(3)
                await client.send_message(cannel_bgm_cache, "!halloween_poker_bgm_stop")
                await asyncio.sleep(27)
                GLOBAL_REACTION_ICON = 0
                TRICK_OR_TREAT_TIME_POKER_REGIST_LIST.clear()
                print("GLOBAL_UNKO_JACK_MODE Falseに代入")
                GLOBAL_UNKO_JACK_MODE["JACK"] = False
                GLOBAL_JACK_ACTING = False


async def ending_scroll_sanka(svr, ret_message, em, channel):

    member_of_on_calk = {}
    poop_member = None
    for m in list(svr.members):
        member_of_on_calk[m.id] = m.display_name

    dirlist = os.listdir("./DataHalloweenPokerInfo")
    
    all_result_hash = {}
    # print(dirlist)
    for d in dirlist:
        path = "./DataHalloweenPokerInfo/" + d
        
        try:
            with open(path, "r") as fr:
                pokerinfo = json.load(fr)

            amount = 0
            id = pokerinfo["id"]
            
            for v in pokerinfo["amount"].values():
                amount = amount + v
                
            all_result_hash[id] = {"amount":amount, "count":len(pokerinfo["cardhistory"]) }
                
        except Exception as e2:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e2.__traceback__))
            print("例外:calc_of_all_poker")
            
    sorted_list = sorted(all_result_hash.items(), key=lambda x: x[1]["amount"], reverse=True )

    modified_sorted_list = []
    for sl in sorted_list:
        if sl[0] in member_of_on_calk:
            modified_sorted_list.append(sl)

    result_str = ""

    index_list_ix = 1
    
    result_channel = get_poker_result_channel(svr)
    await client.send_message(result_channel, "**参加メンバー**")
    
    span_time = 130 / (len(modified_sorted_list)/5)
    print("スパンタイム" + str(span_time))
    for s in modified_sorted_list:
        try:
            result_str = result_str + "🎃 <@" + str(s[0]) + "> \n　　└ " + str(s[1]["count"]) +" 回、 " + str(s[1]["amount"]) + " BDA" + "\n"
            if index_list_ix >= 5 or s is modified_sorted_list[-1]:
                index_list_ix = 0
                em.clear_fields()
                em.add_field(name="参加メンバー", value=result_str, inline=False)
                # em.set_image(url=get_jack_o_lantern_to_ending(svr, 99, "11th"))
                await client.edit_message(ret_message, embed=em)
                await client.send_message(result_channel, result_str)
                # await client.send_message(channel, result_str)
                await asyncio.sleep(span_time)
                result_str = ""
                
                if s is modified_sorted_list[-1]:
                    break
        except Exception as e3:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e3.__traceback__))
            print("例外:calc_of_all_poker")
                
        index_list_ix = index_list_ix + 1





def get_boss_icon(server):
    if '443637824063930369' in server.id: # BDA鯖
        return "https://media.discordapp.net/attachments/498183493361205278/506563026166480896/boss_disappear_icon.png"
    else:
        return "https://media.discordapp.net/attachments/498162384716955655/506562937985433610/boss_disappear_icon.png"


def get_jack_o_lantern_to_close(server, mode=0):
    if mode==2:
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/504350081969946636/jack-o-lantern-to-close-danbo.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/504350376221212672/jack-o-lantern-to-close-danbo.png"
    if mode==7:
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/505322103797710849/chracter_toilet_close.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/505323740532572161/chracter_toilet_close.png"



def get_jack_o_lantern_to_ending(server, mode=0, custom=""):
    # エンディング
    if mode==99:
        if custom == "1st":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506541555813842971/jack-o-lantern-to-r-direct-phone.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506533407430541352/jack-o-lantern-to-r-directi.png"
        if custom == "2nd":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506541574520438784/jack-o-lantern-to-l-direct-phone.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506533444390617108/jack-o-lantern-to-l-directi.png"
                
        if custom == "3rd":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/498330369213333504/jack-o-lantern-to-r-direction.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/498333423195389965/jack-o-lantern-to-r-direction.png"
                
        if custom == "4th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506736558054047744/chracter_toilet_close_ok.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506736616199421952/chracter_toilet_close_ok.png"
        if custom == "5th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/505322210114797568/jack-o-lantern-toilet-3rd.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/505323815124074496/jack-o-lantern-toilet-3rd.png"
        if custom == "6th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/505322182256099329/jack-o-lantern-toilet-2nd.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/505323789731495938/jack-o-lantern-toilet-2nd.png"
        if custom == "7th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/505322141978329088/jack-o-lantern-toilet-1st.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/505323768781078529/jack-o-lantern-toilet-1st.png"
        if custom == "8th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/505322182256099329/jack-o-lantern-toilet-2nd.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/505323789731495938/jack-o-lantern-toilet-2nd.png"
        if custom == "9th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/505322141978329088/jack-o-lantern-toilet-1st.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/505323768781078529/jack-o-lantern-toilet-1st.png"
        if custom == "10th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506740426007379968/jack-o-lantern-toilet-only.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506740697156812801/jack-o-lantern-toilet-only.png"

        if custom == "toumei":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506859050353295370/toumei_large.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506859380801798144/toumei_large.png"

        if custom == "11th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506781913814532096/ending_rolling_member.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506782071209984001/ending_rolling_member.png"

        if custom == "12th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506794101589409827/chosyo.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506793960593948694/chosyo.png"

        if custom == "fin_half":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506794506469900298/fin_fading.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506794756660264960/fin_fading.png"

        if custom == "fin_full":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506859000009326603/fin_full.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506859360748699679/fin_full.png"

        if custom == "fin_black":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506798020004806656/fin_black.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506797936521510915/fin_black.png"


        if custom == "coin":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/504935878225821697/BraveDiamondAceJackCoin.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/504930086433194181/BraveDiamondAceJackCoin.png"


def get_jack_o_lantern_to_yamitojo(server, mode=0, custom=""):
    # やみ登場
    if mode==98:
        if custom == "1st":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506528274499764226/escape_yellow_mini.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506526515320848388/escape_yellow_mini.png"
        elif custom == "2nd":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506528300697649152/escape_sky_mini.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506526552910200854/escape_sky_mini.png"
        elif custom == "3rd":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506528321153007617/escape_pink_mini.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506526726810238976/escape_pink_mini.png"
        elif custom == "4th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506528344066621440/escape_purple_mini.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506526752143704064/escape_purple_mini.png"
        elif custom == "5th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506528363301830657/escape_orange_mini.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506526773144715278/escape_orange_mini.png"
        elif custom == "6th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506528379860680714/escape_green_mini.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506526836038172688/escape_green_mini.png"
        elif custom == "7th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506558431360974851/boss_disappear_01.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506556582335873047/boss_disappear_01.png"
        elif custom == "8th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506558456157831184/boss_disappear_02.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506556611167256578/boss_disappear_02.png"
        elif custom == "9th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506558483911409709/boss_disappear_03.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506556645011095552/boss_disappear_03.png"
        elif custom == "10th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506563844911530015/boss_disappear_04.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506563736534908930/boss_disappear_04.png"
        elif custom == "11th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506563868789833768/boss_disappear_05.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506563768617140235/boss_disappear_05.png"
        elif custom == "12th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506566664620343314/boss_disappear_06.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506566597658411028/boss_disappear_06.png"
        elif custom == "25th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506582528841482266/boss_disappear_22.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506582692238983178/boss_disappear_22.png"
                
        elif custom == "13th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/498330369213333504/jack-o-lantern-to-r-direction.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/498333423195389965/jack-o-lantern-to-r-direction.png"
        elif custom == "14th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/498330385764319272/jack-o-lantern-to-l-direction.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/498333594075267083/jack-o-lantern-to-l-direction.png"
        elif custom == "15th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506511557425889280/weapon_close_box.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506515359382241280/weapon_close_box.png"
        elif custom == "16th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506511484222701578/weapon_prev_oden.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506515333310447618/weapon_prev_oden.png"
        elif custom == "17th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506511584625950722/weapon_post_odin.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506515381217656841/weapon_post_odin.png"
        elif custom == "18th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506511686291816463/weapon_prev_kasa.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506515431620739088/weapon_prev_kasa.png"
        elif custom == "19th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506511728956276737/weapon_post_shield.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506515531504025620/weapon_post_shield.png"
        elif custom == "20th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506511812859265044/weapon_prev_okan.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506515639150706698/weapon_prev_okan.png"
        elif custom == "21th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506513424495149056/weapon_post_angel.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506515705399869441/weapon_post_angel.png"
        elif custom == "23th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506514584413274112/omega-jack-o-lantern.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506515748810915870/omega-jack-o-lantern.png"
        elif custom == "26th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506588798847811591/boss_disappear_26.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506589127181991946/boss_disappear_26.png"
        elif custom == "27th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/506588826622492672/boss_disappear_27.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/506589147419639819/boss_disappear_27.png"







def get_jack_o_lantern_to_toilet(server, mode=0, custom=""):
    # トイレ
    if mode==7:
        if custom == "1st":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/505322141978329088/jack-o-lantern-toilet-1st.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/505323768781078529/jack-o-lantern-toilet-1st.png"
        elif custom == "2nd":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/505322182256099329/jack-o-lantern-toilet-2nd.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/505323789731495938/jack-o-lantern-toilet-2nd.png"
        elif custom == "3rd":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/505322210114797568/jack-o-lantern-toilet-3rd.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/505323815124074496/jack-o-lantern-toilet-3rd.png"


def get_jack_o_lantern_to_chart(server, mode=0, custom=""):
    # チャート
    if mode==5:
        if custom == "1st":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/505075591670661132/jack-o-lantern-chart-1st.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/505076040251604998/jack-o-lantern-chart-1st.png"
        elif custom == "2nd":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/505075634163286029/jack-o-lantern-chart-2nd.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/505076058282786846/jack-o-lantern-chart-2nd.png"
        elif custom == "3rd":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/505075675934490654/jack-o-lantern-chart-3rd.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/505076075483627545/jack-o-lantern-chart-3rd.png"
        elif custom == "4th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/505075740702801921/jack-o-lantern-chart-4th.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/505076095159107614/jack-o-lantern-chart-4th.png"
        elif custom == "5th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/505075808381960220/jack-o-lantern-chart-5th.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/505076112850944001/jack-o-lantern-chart-5th.png"
        elif custom == "6th":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/505081200293969923/jack-o-lantern-chart-6th.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/505081481111142421/jack-o-lantern-chart-6th.png"


def get_jack_o_lantern_to_r_direction_kasa(server, mode=0, custom=""):

    # 傘
    if mode==4:
        if custom == "blue":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/504998041007161356/jack-o-lantern-to-r-direction-kasa-blue.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/504998833789337630/jack-o-lantern-to-r-direction-kasa-blue.png"
        
        elif custom == "green":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/504998070052847627/jack-o-lantern-to-r-direction-kasa-green.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/504998851732701191/jack-o-lantern-to-r-direction-kasa-green.png"

        elif custom == "red":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/504998100927250433/jack-o-lantern-to-r-direction-kasa-red.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/504998870388965387/jack-o-lantern-to-r-direction-kasa-red.png"

        elif custom == "orange":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/504998127988768788/jack-o-lantern-to-r-direction-kasa-orange.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/504998891905744897/jack-o-lantern-to-r-direction-kasa-orange.png"

        elif custom == "orange_kaze":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/504998545779064832/jack-o-lantern-to-r-direction-kasa-orange-kaze.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/504999003352727553/jack-o-lantern-to-r-direction-kasa-orange-kaze.png"


def get_jack_o_lantern_to_l_direction_kasa(server, mode=0, custom=""):

    # 傘
    if mode==4:
        if custom == "blue":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/504998153863561226/jack-o-lantern-to-l-direction-kasa-blue.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/504998909353918475/jack-o-lantern-to-l-direction-kasa-blue.png"
        
        elif custom == "green":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/504998174767710229/jack-o-lantern-to-l-direction-kasa-green.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/504998926374666261/jack-o-lantern-to-l-direction-kasa-green.png"

        elif custom == "red":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/504998197995896833/jack-o-lantern-to-l-direction-kasa-red.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/504998940576448522/jack-o-lantern-to-l-direction-kasa-red.png"

        elif custom == "orange":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/504998241742356480/jack-o-lantern-to-l-direction-kasa-orange.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/504998961275469831/jack-o-lantern-to-l-direction-kasa-orange.png"

        elif custom == "orange_up":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/504998429705895936/jack-o-lantern-to-l-direction-kasa-orange_up.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/504998977801027595/jack-o-lantern-to-l-direction-kasa-orange_up.png"

        elif custom == "orange_kaze":
            if '443637824063930369' in server.id: # BDA鯖
                return "https://media.discordapp.net/attachments/498183493361205278/504998567732183040/jack-o-lantern-to-l-direction-kasa-orange-kaze.png"
            else:
                return "https://media.discordapp.net/attachments/498162384716955655/504999020184207360/jack-o-lantern-to-l-direction-kasa-orange-kaze.png"



def get_jack_o_lantern_to_r_direction_shower(server, mode=0):

    # シャワー
    if mode==3:
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/504631106507898920/jack-o-lantern-to-r-direction-shampoo-shawer.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/504638670595162132/jack-o-lantern-to-r-direction-shampoo-shawer.png"


def get_jack_o_lantern_to_l_direction_shower(server, mode=0):

    # シャワー
    if mode==3:
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/504631953488740355/jack-o-lantern-to-l-direction-shampoo-shawer.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/504638691520544768/jack-o-lantern-to-l-direction-shampoo-shawer.png"


def get_jack_o_lantern_to_r_direction(server, mode=0):

    # king
    if mode==1:
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/504304286566580239/jack-o-lantern-to-r-direction-king.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/504304528334520320/jack-o-lantern-to-r-direction-king.png"
    elif mode==2:
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/504350105714032641/jack-o-lantern-to-r-direction-danbo.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/504350399608913948/jack-o-lantern-to-r-direction-danbo.png"
    elif mode==3: # シャワー
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/504630431963021312/jack-o-lantern-to-r-direction-shampoo.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/504638614878289930/jack-o-lantern-to-r-direction-shampoo.png"
    elif mode==6: # おでん
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/505265899016552453/jack-o-lantern-to-r-direction-oden.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/505270172827910154/jack-o-lantern-to-r-direction-oden.png"
    

    if GLOBAL_UNKO_JACK_MODE["JACK"]:
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/501761156000514048/jack-o-lantern-to-r-direction-unko.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/501758880225689601/jack-o-lantern-to-r-direction-unko.png"
    else:
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/498330369213333504/jack-o-lantern-to-r-direction.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/498333423195389965/jack-o-lantern-to-r-direction.png"

def get_jack_o_lantern_to_l_direction(server, mode=0):

    # king
    if mode==1:
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/504304318422319134/jack-o-lantern-to-l-direction-king.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/504304547703947275/jack-o-lantern-to-l-direction-king.png"
    elif mode==2:
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/504350128404955136/jack-o-lantern-to-l-direction-danbo.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/504350419544178689/jack-o-lantern-to-l-direction-danbo.png"
    elif mode==3: # シャワー
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/504630483683115008/jack-o-lantern-to-l-direction-shampoo.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/504638636847792128/jack-o-lantern-to-l-direction-shampoo.png"
    elif mode==6: # おでん
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/505265963713691651/jack-o-lantern-to-l-direction-oden.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/505270197230239745/jack-o-lantern-to-l-direction-oden.png"


    if GLOBAL_UNKO_JACK_MODE["JACK"]:
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/501808829101768735/jack-o-lantern-to-l-direction-unko.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/501808394114695171/jack-o-lantern-to-l-direction-unko.png"
    else:
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/498330385764319272/jack-o-lantern-to-l-direction.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/498333594075267083/jack-o-lantern-to-l-direction.png"


def get_jack_o_lantern_trick_or_treat(server, mode=0):

    # king
    if mode==1:
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/504304347891367948/trick_or_treat-king.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/504304565059977232/trick_or_treat-king.png"
    elif mode==2:
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/504350169786220565/trick_or_treat-danbo.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/504350442936074240/trick_or_treat-danbo.png"
    elif mode==3: # シャワー
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/504637851447590922/trick_or_treat-shampoo-no-shower.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/504638750601642025/trick_or_treat-shampoo-no-shower.png"
    elif mode==4: # 傘
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/504998621557817344/trick_or_treat-kasa.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/504999056477650944/trick_or_treat-kasa.png"
    # チャート
    elif mode==5:
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/505081229469679617/jack-o-lantern-chart-trick-or-treat.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/505081496743313409/jack-o-lantern-chart-trick-or-treat.png"
    elif mode==6: # おでん
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/505266096518070287/trick_or_treat-oden.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/505270237101424641/trick_or_treat-oden.png"
    elif mode==7: # トイレ
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/505327535119269888/trick_or_treat_toilet.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/505323893003780106/trick_or_treat_toilet.png"

    if GLOBAL_UNKO_JACK_MODE["JACK"]:
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/501761194755883028/trick_or_treat-unko.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/501759024870588416/trick_or_treat-unko.png"
    else:
        if '443637824063930369' in server.id: # BDA鯖
            return "https://media.discordapp.net/attachments/498183493361205278/498330403447504897/trick_or_treat.png"
        else:
            return "https://media.discordapp.net/attachments/498162384716955655/498334187565350934/trick_or_treat.png"

def get_pumpkin_unko_picture(server):
    if '443637824063930369' in server.id: # BDA鯖
        return "https://media.discordapp.net/attachments/498183493361205278/501761136262250496/pumpkin-unko.png"
    else:
        return "https://media.discordapp.net/attachments/498162384716955655/501758815235080202/pumpkin-unko.png"


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


async def calc_of_all_poker(target_channel_obj, this_time_list, poop):
    member_of_on_calk = {}
    poop_member = None
    for m in list(target_channel_obj.server.members):
        if poop == m.id:
            poop_member = m
            
        member_of_on_calk[m.id] = m.display_name
    
    # ch = get_ether_regist_channel(target_channel_obj)
    
    dirlist = os.listdir("./DataHalloweenPokerInfo")
    
    
    all_result_hash = {}
    # print(dirlist)
    for d in dirlist:
        path = "./DataHalloweenPokerInfo/" + d
        
        try:
            with open(path, "r") as fr:
                pokerinfo = json.load(fr)

            amount = 0
            id = pokerinfo["id"]
            
            for v in pokerinfo["amount"].values():
                amount = amount + v
                
            all_result_hash[id] = amount
                
        except Exception as e2:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e2.__traceback__))
            print("例外:calc_of_all_poker")
            
    sorted_list = sorted(all_result_hash.items(), key=lambda x: x[1], reverse=True )

    modified_sorted_list = []
    for sl in sorted_list:
        if sl[0] in member_of_on_calk:
            modified_sorted_list.append(sl)

    result_str = "─ **総計**の結果 ─\n　(The result of **total** time)\n\n"

    index_list_ix = 0
    for s in modified_sorted_list:
        index_list_ix = index_list_ix + 1
        if len(modified_sorted_list) >=100:
            number_padding = "{0:03d}".format(index_list_ix)
        elif len(modified_sorted_list) >=10:
            number_padding = "{0:02d}".format(index_list_ix)
        else:
            number_padding = str(index_list_ix)
        
        # 強制的に消しておく
        medal = ""
        
        # 今参加していたら、メンション
        if s[0] in this_time_list:
        
            result_str = result_str + number_padding + ". " + medal + " <@" + str(s[0]) + ">" + "      " + str(s[1]) + " BDA.\n"
        # 今不参加なら文字列
        else:
            result_str = result_str + number_padding + ". " + medal + "  @" + member_of_on_calk[s[0]] + "      " + str(s[1]) + " BDA.\n"

        if index_list_ix >= 30:
            # その他にいたら略する
            if len(modified_sorted_list) > 30:
                result_str = result_str + "...その他(Others) " + str(len(modified_sorted_list)-index_list_ix) + " 人\n"

            break

    if poop_member:
        try:
            em = update_one_halloween_poker_jack_unko(target_channel_obj, poop_member)

            return result_str, em
        except Exception as e2:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e2.__traceback__))
            print("例外:update_one_halloween_poker_jack_unko")
            return result_str, None
    else:
        return result_str, None


def get_hand_names():
    '''
    Sample n random hands and print a table of percentages for each type of hand.
    '''
    hand_names = ('ブタ -High Card-', 'ワンペア -1 Pair-', 'ツーペア -2 Pairs-', 'スリーカード -3 Kind-', 'ストレート -Straight-', 'フラッシュ -Flush-', 'フルハウス -Full House-', 'フォーカード -4 Kind-', 'ストレートフラッシュ -Straight Flush-')
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
    red_joker_cards =  [r+s for r in '23456789TJQKA' for s in 'HD']
    jokers = ['?B', '?R' ]

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
    




def get_today_datestring(message):
    #今日の日付の作成
    date = message.timestamp.now()
    strdate = str(date.year) + '{0:02d}'.format(date.month) + '{0:02d}'.format(date.day)
    return strdate


def get_url_of_hallowine_cards_base(message):
    if "BDA" in message.channel.server.name:
        return "https://media.discordapp.net/attachments/498183493361205278/498183608679268359/hallowine_cards_base.png"
    else:
        return "https://media.discordapp.net/attachments/498162384716955655/498184214886481950/hallowine_cards_base.png"

async def member_hand_percenteges(message):
    
    global TRICK_OR_TREAT_CHANNEL

    global GLOBAL_START_MESSAGE
    global GLOBAL_CLOSE_MESSAGE

    global GLOBAL_REACTION_ICON

    # 入力タイミングではない
    if not TRICK_OR_TREAT_CHANNEL:
        return False

    # チャンネルが違う
    if TRICK_OR_TREAT_CHANNEL.id != message.channel.id:
        return False

    # 値が有効で、
    if GLOBAL_START_MESSAGE and int(message.id) < int(GLOBAL_START_MESSAGE):
        print("早い投稿")
        return False

    # 遅い投稿
    if GLOBAL_CLOSE_MESSAGE and int(GLOBAL_CLOSE_MESSAGE) < int(message.id) :
        print("遅い投稿")
        return False
    
    # ETHアドレスに登録がある。
    if not os.path.exists("../Diatan/DataMemberInfo/" + str(message.author.id) + ".json"):
        eth_ch = get_ether_regist_channel(message)
        await report_error(message, "登録情報がないぜぃ？\n" + "<#" + eth_ch.id + ">" + " に\n自分の **MyEtherWallet** など、\nエアドロが受け取れるETHウォレットアドレスを投稿して、\n**コインを受け取れるように**するのがいいぜぃ？")
        return False
        
    # ハッピーハロウィンの言葉的なものを入力してる？
    if not IsInputHappyHalloWeenWords(message.content):
        return False
    
    # もう入力済み
    if message.author.id in TRICK_OR_TREAT_TIME_POKER_REGIST_LIST:
        print("入力済み")
        print(str(TRICK_OR_TREAT_TIME_POKER_REGIST_LIST))
        return False
    
    if not has_post_data(message):
        await make_one_halloween_poker_data(message)
    
    hand_names = get_hand_names()

    
    all_cards = get_all_cards()
    # 5枚をランダムに
    cards = random.sample(all_cards, 5)
    
    # cards = "9D 3D 2C AC 5C".split(" ")
    
    bests = poker.best_wild_hand(cards)
    rank = poker.hand_rank(bests)
    
    try:
        # 60以上のリアクション評価値
        if GLOBAL_REACTION_ICON > 60:
            # 多ければ多いほど、なんども手札を引いて一番いいものが採用される
            kurikaeshi_count = GLOBAL_REACTION_ICON // 30
            for kuri in range(0, kurikaeshi_count):
                # 5枚をランダムに
                cards2 = random.sample(all_cards, 5)
                bests2 = poker.best_wild_hand(cards2)
                rank2 = poker.hand_rank(bests2)
                if rank2 > rank:
                    cards = cards2
                    bests = bests2
                    rank = rank2
    except:
        print("カード繰り返しエラー")
    
    if rank[0] == 0 and sum(rank[1]) <= 31:
        print("31以下")
        if (not "9D" in bests) and (random.randint(1, 16) == 2):
            sorted_cards = sorted(bests)
            cards = [sorted_cards[0], sorted_cards[1], sorted_cards[2], sorted_cards[3], "9D"]
            random.shuffle(cards)
            bests = poker.best_wild_hand(cards)
            rank = poker.hand_rank(bests)
    
    rank_1st = rank[0]
    rank_2nd = 0

    display_cards = best_wild_hand_reflect_hands(cards, bests)
    path, path2 = make_png_img(message, display_cards)

    # print("rank:" + str(rank))

    try:
        get_bda_point = rank_1st
        
        # 豚なら
        if get_bda_point == 0:
            highcard = sum(rank[1])
            get_bda_point = get_bda_point + highcard
        
        # 豚以外なら
        else:
            get_bda_point = get_bda_point * get_bda_point * 100
    
        get_bda_jack_point = 0
        if "AD" in bests:
            get_bda_jack_point = get_bda_jack_point + 500
        if (display_cards[0] == "WJB" and display_cards[1] == "WJR") or (display_cards[1] == "WJB" and display_cards[2] == "WJR") or (display_cards[2] == "WJB" and display_cards[3] == "WJR") or (display_cards[3] == "WJB" and display_cards[4] == "WJR"):
            get_bda_jack_point = get_bda_jack_point + 30000
            
        total_point = get_bda_point+get_bda_jack_point
        await update_one_halloween_poker_data(message, rank_1st, bests, total_point)
    except Exception as e2:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e2.__traceback__))
        print("例外:update_one_halloween_poker_data")
        

    modified_display_cards = get_symbol_display_cards(display_cards)
    str_tehuda = "  ,  ".join(modified_display_cards)

    TRICK_OR_TREAT_TIME_POKER_REGIST_LIST[message.author.id] = {"bests":bests, "point":total_point}

#    f = discord.File(path, filename=path2)
    cache_channel = get_poker_cache_count_channel(message.author)
    content_message = "..."
    send_message_obj = await client.send_file(cache_channel, path, content=content_message, filename=path2)
    
    try:
        em = discord.Embed(title="", description="", color=0xDEED33)
        em.add_field(name="ハロウィンポーカー -The Halloween in Poker-", value= "<@" + message.author.id + ">", inline=False)
        str_tehuda = "  ,  ".join(modified_display_cards)
        avator_url = message.author.avatar_url or message.author.default_avatar_url
        avator_url = avator_url.replace(".webp?", ".png?")
        em.set_thumbnail(url=avator_url)
        em.set_image(url=get_url_of_hallowine_cards_base(message))
            
        ret = None
        try:
            ret = await client.send_message(message.channel, embed=em)
        except:
            ret = None
        
        if ret == None:
            try:
                await asyncio.sleep(1)
                ret = await client.send_message(message.channel, embed=em)
            except:
                ret = None

        if ret == None:
            try:
                await asyncio.sleep(1)
                ret = await client.send_message(message.channel, embed=em)
            except:
                ret = None
            
        proxy_url = send_message_obj.attachments[0]["proxy_url"]
        await asyncio.sleep(3)
        em.set_image(url=proxy_url)
        
        if get_bda_point == 0:
            em.add_field(name=hand_names[rank_1st], value="-", inline=False)
        else:
            em.add_field(name=hand_names[rank_1st], value=str(get_bda_point)  + " BDA Get!!", inline=False)
        if get_bda_jack_point > 0:
            em.add_field(name="Jack-o-Lantern Bonus!!", value=str(get_bda_jack_point) + " BDA Get!!", inline=False)
        em.set_footer(text=str_tehuda)
        
        ret_edit = None
        
        try:
            ret_edit = await client.edit_message(ret, embed=em)
        except:
            ret_edit = None
            
        if ret_edit == None:
            try:
                await asyncio.sleep(1)
                ret_edit = await client.edit_message(ret, embed=em)
            except:
                ret_edit = None

        if ret_edit == None:
            try:
                await asyncio.sleep(1)
                ret_edit = await client.edit_message(ret, embed=em)
            except:
                ret_edit = None
            
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
    if len(list(files)) > 1000:
        for file in files:
            try:
                m = re.search("^[0-9]+", file)
                # print(str(m))
                date = m.group(0)
                # print(date)
                date = int(date)
                
                # 現在のunixタイムを出す
                now = datetime.datetime.now()
                unix = now.timestamp()
                unix = int(unix)

                if unix-date > 600:
                    os.remove('DataTempImage/' + file)
                
            except:
                print(sys.exc_info())



# ハッピーハロウィンの文言を入力したのか？
def IsInputHappyHalloWeenWords(text):
    similar1 = get_sequence_matcher_coef(text.upper(), "Happy Halloween!".upper())
    similar2 = get_sequence_matcher_coef(text, "ハッピーハロウィン")
    similar3 = get_sequence_matcher_coef(text, "はっぴーはろうぃん")
    similar4 = get_sequence_matcher_coef(text, "ハッピーはろうぃん")
    similar5 = get_sequence_matcher_coef(text, "はっぴーハロウィン")
    similar6 = get_sequence_matcher_coef(text, "ﾊｯﾋﾟｰﾊﾛｳｨﾝ")
    similar7 = get_sequence_matcher_coef(text.upper(), "Halloween!".upper())
    similar8 = get_sequence_matcher_coef(text, "ハロウィン")
    similar9 = get_sequence_matcher_coef(text, "はろうぃん")
    similar10 = get_sequence_matcher_coef(text, "ﾊﾛｳｨﾝ")
    if similar1 > 0.5 or similar2 > 0.5 or similar3 > 0.5 or similar4 > 0.5 or similar5 > 0.5 or similar6 > 0.5 or similar7 > 0.5 or similar8 > 0.5 or similar9 > 0.5 or similar10 > 0.5 :
        return True
    elif "ハロウィン" in text:
        return True
    elif "はろうぃん" in text:
        return True
    elif "Halloween" in text:
        return True
    elif ":jack_o_lantern:" in text:
        return True
    else:
        return False



def get_data_halloween_poker_path(message):
    id = message.author.id
    return 'DataHalloweenPokerInfo/' + str(id) + ".json"


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


async def update_one_halloween_poker_data(message, rank, cards, get_bda_point):
    try:

        path = get_data_halloween_poker_path(message)
        # print(path)
        with open(path, "r") as fr:
            pokerinfo = json.load(fr)

        pokerinfo["cardhistory"].append([rank, cards])
        today_string = get_today_datestring(message)
        
        # キーがなければ作成
        if not today_string in pokerinfo["amount"]:
            pokerinfo["amount"][today_string] = 0

        pokerinfo["amount"][today_string] = pokerinfo["amount"][today_string] + get_bda_point

        path = get_data_halloween_poker_path(message)
        json_data = json.dumps(pokerinfo, indent=4)
        with open(path, "w") as fw:
            fw.write(json_data)
        return True

    except:
        await report_error(message, "update_one_halloween_poker_dataデータ作成中にエラー")
        await report_error(message, sys.exc_info())
    
    return False


def update_one_halloween_poker_jack_unko(target_channel_obj, member):
    try:

        path = 'DataHalloweenPokerInfo/' + member.id + ".json"
        # print(path)
        with open(path, "r") as fr:
            pokerinfo = json.load(fr)

        # キーがなければ作成
        if not "poop" in pokerinfo:
            pokerinfo["poop"] = []

        now = datetime.datetime.now()
        unix = now.timestamp()
        unix = int(unix)

        rand_cnt = random.randint(1, 3)
        pokerinfo["poop"].append( {str(unix):rand_cnt} )

        path = 'DataHalloweenPokerInfo/' + member.id + ".json"
        json_data = json.dumps(pokerinfo, indent=4)
        with open(path, "w") as fw:
            fw.write(json_data)

        em = discord.Embed(title="", description="", color=0x36393f)
        em.set_image(url=get_pumpkin_unko_picture(target_channel_obj.server))
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





@client.event
async def on_reaction_add(reaction, user):

    global GLOBAL_REACTION_ICON
    global GLOBAL_REACTION_ICON_ROCK
    
    # ロックがかかっていないならば…
    if GLOBAL_REACTION_ICON_ROCK == False:
        if reaction.emoji == '👉':
            GLOBAL_REACTION_ICON = GLOBAL_REACTION_ICON + 2
        elif reaction.emoji == '👈':
            GLOBAL_REACTION_ICON = GLOBAL_REACTION_ICON + 2
        elif reaction.emoji == '👑':
            GLOBAL_REACTION_ICON = GLOBAL_REACTION_ICON + 5
        elif reaction.emoji == '📦':
            GLOBAL_REACTION_ICON = GLOBAL_REACTION_ICON + 5
        elif reaction.emoji == '🚿':
            GLOBAL_REACTION_ICON = GLOBAL_REACTION_ICON + 5
        elif reaction.emoji == '🎃':
            GLOBAL_REACTION_ICON = GLOBAL_REACTION_ICON + 5
        elif reaction.emoji == '☂':
            GLOBAL_REACTION_ICON = GLOBAL_REACTION_ICON + 3
        elif reaction.emoji == '📈':
            GLOBAL_REACTION_ICON = GLOBAL_REACTION_ICON + 5
        elif reaction.emoji == '📉':
            GLOBAL_REACTION_ICON = GLOBAL_REACTION_ICON + 1
        elif reaction.emoji == '🍢':
            GLOBAL_REACTION_ICON = GLOBAL_REACTION_ICON + 5
        elif reaction.emoji == '🚽':
            GLOBAL_REACTION_ICON = GLOBAL_REACTION_ICON + 5
        elif reaction.emoji == '🚾':
            GLOBAL_REACTION_ICON = GLOBAL_REACTION_ICON + 5
        elif reaction.emoji == '🦇':
            GLOBAL_REACTION_ICON = GLOBAL_REACTION_ICON + 5
        elif GLOBAL_REACTION_ICON > 0:
            GLOBAL_REACTION_ICON = GLOBAL_REACTION_ICON + 1

# メッセージを受信するごとに実行される
@client.event
async def on_message(message):

    global PRE_DATETIME_HOUR
    global TRICK_OR_TREAT_CHANNEL
    global GLOBAL_START_MESSAGE
    global GLOBAL_CLOSE_MESSAGE
    global GLOBAL_JACK_ACTING
    
    # komiyamma
    if message.author.id == "397238348877529099":
        # そのチャンネルに存在するメッセージを全て削除する
        if message.content.startswith('!-!-!clear'):
            tmp = await client.send_message(message.channel, 'チャンネルのメッセージを削除しています')
            try:
                async for msg in client.logs_from(message.channel):
                    await client.delete_message(msg)
            except:
                print("削除中にエラーが発生しました")
            return


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


    if message.content == "!halloween poker":
    
        if message.author.id in ["397238348877529099", "443634644294959104", "446297147957182464", "444624675251814422", "427792548568760321", "429920700359245824", "295731360776060939" ,"427257154542501927"]:
            print("強制発動")
            # ジャックー・オー・ランタンが演技や統計まで一連の何かをしている
            # 間であれば、やらないが、それ以外なら、ハロウィンポーカーを再度
            if not GLOBAL_JACK_ACTING:
                PRE_DATETIME_HOUR = -1
            else:
                print("アクション中")

    try:
        if message.content.upper() == "!JACK":
            print("ジャックモードチェック")
            # ジャックー・オー・ランタンが演技や統計まで一連の何かをしている
            # 間であれば、やらないが、それ以外なら、ハロウィンポーカーを再度
            # 安全のため、55分～5分の間はやらない。
            nowdatetime = datetime.datetime.now()

            has_unko_card_count = await load_one_halloween_poker_jack_unko(message)
            if has_unko_card_count > 0:

                target_channel_name = get_target_channel_name_list()
                if not GLOBAL_JACK_ACTING and 6 <= nowdatetime.minute and nowdatetime.minute <= 54 and target_channel_name and (message.channel.name in target_channel_name):
                    PRE_DATETIME_HOUR = -1
                    print("GLOBAL_UNKO_JACK_MODE Trueに代入")
                    GLOBAL_UNKO_JACK_MODE["JACK"] = True
                    remain_count = await decrement_one_halloween_poker_jack_unko(message)
                     
                else:
                    em = discord.Embed(title="", description="", color=0x36393f)
                    em.set_image(url=get_pumpkin_unko_picture(message.channel.server))
                    em.add_field(name="返信相手 (reply)", value= "<@" + message.author.id + ">", inline=False)
                    em.add_field(name="あなたの「!JACK」(Your's ❝!JACK❞) ", value="残り" + str(has_unko_card_count) + " 回" + " (remaining)", inline=False)
                    em.set_footer(text="今はその時ではないようだ...(It is not the time now...)")
                    
                    await client.send_message(message.channel, embed=em)
    except Exception as e5:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e5.__traceback__))
        print("例外:!JACK error")


    try:

        is_success = await member_hand_percenteges(message)

    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
        print("例外:poker hand_percenteges error")


    try:
        if message.channel.name in get_target_channel_name_list():
            delete_old_image(message)
            
    except Exception as e:
        pass







# APP(BOT)を実行
client.run(BOT_TOKEN)
#