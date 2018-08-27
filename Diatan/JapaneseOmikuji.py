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


def is_permission_omikuji_condition(message):
    ch = str(message.channel)
    if ch in ["★おみくじコーナー★"]:
       return True
    if re.match("ディアたんと会話", ch) and (random.randint(1,10) < 3):
       return True
       
    return False


def is_omikuji_command(text):
    if text == 'おみくじ' or text == 'みくじ' :
        return True

    okword_list = [
        'みくじ引いて', 'みくじを引いて',
        'みくじひいて', 'みくじをひいて',
        'みくじ引け', 'みくじを引け',
        'みくじひけ', 'みくじをひけ',
        'みくじ引く', 'みくじを引く',
        'みくじひく', 'みくじをひく',
        'みくじひく', 'みくじをひく',
        'みくじよろ', 'みくじをよろ',
        'みくじだよ',
        'みくじして', 'みくじをして',
        'みくじしよう', 'みくじをしよう',
        'みくじしよっか', 'みくじをしよっか',
        'みくじしろ', 'みくじをしろ',
        'みくじせよ', 'みくじをせよ',
        'みくじはよ', 'みくじをはよ',
        'みくじする', 'みくじをする',
        'みくじします', 'みくじをします',
        'みくじやろ', 'みくじをやろ',
        'みくじやって', 'みくじをやって',
        'みくじお願い', 'みくじをお願い',
        'みくじおねがい', 'みくじをおねがい',
    ]
    
    for ok_word in okword_list:
        if ok_word in text:
            return True
    
    return False



DirDataJapaneseOmikuji = "DataJapaneseOmikuji"

def get_date_omikuji_file(date):
    global DirDataJapaneseOmikuji
    fullpath = DirDataJapaneseOmikuji + "/" + date + ".txt"
    return fullpath
    
def is_exist_today_omikuji_file(date):
    fullpath = ""
    try:
        fullpath = get_date_omikuji_file(date)
        if os.path.exists(fullpath):
            return True
        else:
            return False
    except:
        pass
    
    return False

def get_today_omikuji_data(date):
    fullpath = get_date_omikuji_file(date)
    try:
        with open(fullpath,'r') as fr:
            json_data = json.load(fr)
        return json_data
    except:
        pass
        
    return False

def save_today_omikuji_data(date, dict):
    fullpath = get_date_omikuji_file(date)
    
    try:
        json_data = json.dumps(dict, indent=4)
        with open(fullpath,'w') as fw:
            fw.write(json_data)
        return True
    except:
        pass
    return False

def get_busy_omikuji_message(message):
    em = discord.Embed(title=" ", description="─────────\n" + message.author.display_name, color=0xDEED33)
    em.set_author(name='ディア', icon_url=client.user.default_avatar_url)
    em.set_author(name='ディア', icon_url='http://bdacoin.org/bot/omikuji/image/face.png')
    
    em.add_field(name="只今集計中です!!", value="─────────", inline=False)
    return em

def get_error_omikuji_message(message):
    em = discord.Embed(title=" ", description="─────────\n" + message.author.display_name, color=0xDEED33)
    em.set_author(name='ディア', icon_url=client.user.default_avatar_url)
    em.set_author(name='ディア', icon_url='http://bdacoin.org/bot/omikuji/image/face.png')
    
    em.add_field(name="エラーです!!", value="─────────", inline=False)
    return em



def get_today_datestring(message):
    #今日の日付の作成
    date = message.timestamp.now()
    strdate = str(date.year) + '{0:02d}'.format(date.month) + '{0:02d}'.format(date.day)
    return strdate

def is_busy_timestamp(message):
    #今日の日付の作成
    date = message.timestamp.now()
    if date.hour == 23 and date.minute == 59 and date.second >= 55:
        return True
    if date.hour == 0 and date.minute == 0 and date.second <= 5:
        return True
    
    return False

def get_embedded_omikuji_object(message):

    #今日の日付の作成
    date = message.timestamp.now()
    if is_busy_timestamp(message):
        return get_busy_omikuji_message(message)

    strdate = get_today_datestring(message)
    tstamp = message.timestamp.now()
    print(message.timestamp.now())

    # 今日はじめてで、ファイルが無いならファイル作成
    if not is_exist_today_omikuji_file(strdate):
        first_dict = {
            "date": strdate,
            "大吉": [],
            "吉": [],
            "中吉": [],
            "末吉": [],
            "凶": [],
        }

        result = save_today_omikuji_data(strdate, first_dict)
        if result == False:
            return get_error_omikuji_message(message)
    
    # ファイルがあるので読み込み
    result = get_today_omikuji_data(strdate)
    if result == False:
        return get_error_omikuji_message(message)
    
    un_list = {
        "大吉":"01",
        "吉":"02",
        "中吉":"03",
        "末吉":"04",
        "凶":"05"
    }

    # ハッシュからランダムで１つ選ぶ
    omikuji_key, omikuji_lv = random.choice(list(un_list.items()))
    rnd = random.choice([0,1,2])
    print("rnd:" + str(rnd))
    if rnd >= 1 and (omikuji_key == "大吉" or omikuji_key == "凶"):
        print("ふりなおし")
        omikuji_key, omikuji_lv = random.choice(list(un_list.items()))

    # 該当のメンバーはすでにおみくじを引いているかもしれない
    id = message.author.id
    is_exist = False
    today_omikuji = ""
    for k in result:
        print(k)
        if id in result[k]:
             today_omikuji = k
             
    # 該当のメンバーは今日おみくじを引いている
    if today_omikuji != "":
        print("今日すでに引いたのと同じものへと修正")
        omikuji_key = today_omikuji
        omikuji_lv = un_list[omikuji_key]
    
    # 該当のメンバーは今日はじめておみくじを引いた
    else:
        # ユーザーを足す
        result[omikuji_key].append(id)
        save_today_omikuji_data(strdate, result)

    # 
    em = discord.Embed(title=" ", description="─────────\n" + message.author.display_name + " さんの運勢は ...", color=0xDEED33)
#    em = discord.Embed(title=message.author.display_name + " さんの運勢", description=message.author.display_name + " さんの運勢は... __" + omikuji_key + "__ですよ!!", colour=0xDEED33)
    em.set_author(name='ディア', icon_url=client.user.default_avatar_url)
    em.set_author(name='ディア', icon_url='http://bdacoin.org/bot/omikuji/image/face.png')
    
    em.add_field(name=omikuji_key + "です!!", value="─────────", inline=False)
    
    em.set_thumbnail(url="http://bdacoin.org/bot/omikuji/image/" + omikuji_lv + "_omkj.png")

    em.set_image(url="http://bdacoin.org/bot/omikuji/image/" + omikuji_lv + ".png")
    return em



async def say_embedded_omikuji_message(message):
    if is_omikuji_command(message.content):
        em = get_embedded_omikuji_object(message)
        if em != None:
            await client.send_message(message.channel, embed=em)

        # 簡易だと以下だがデザイン性には欠ける
        # await client.send_message(message.channel, str(message.author.display_name) + "さんの運勢だよ!")
        # img_list = [ "01.png", "02.png", "03.png", "04.png", "05.png" ]

        # １つランダムで選ぶ
        # path = random.choice(img_list)

        # 該当チャンネルに投稿する
        # await client.send_file(message.channel, path)


def is_report_command_condition(command):
    if re.match("^omikujiinfo \d{8}$", command):
        return True


def report_command_one_key_name(json_data, key):
    msg = []
    try:
        for id in json_data[key]:
            msg.append( "<@" + str(id) + ">" )
    except:
        pass

    return " , ".join(msg)

def report_command_one_key_eth(json_data, key):
    msg = []
    try:
        for id in json_data[key]:
            fullpath = "DataMemberInfo/" + str(id) + ".json"
            if os.path.exists(fullpath):
                try:
                    with open(fullpath,'r') as fr:
                        json_data = json.load(fr)
                    msg.append(json_data["eth_address"])
                    
                except:
                    pass
                    
            else:
                msg.append( "<@" + str(id) + ">" )
    except:
        pass

    return '[ "' + '" , "'.join(msg) + '" ]'

async def report_command(message):
    if is_report_command_condition(message.content):
        m = re.search("^omikujiinfo (\d{8})$", message.content)
        date = m.group(1)
        fullpath = get_date_omikuji_file(date)
        if os.path.exists(fullpath):
            json_data = get_today_omikuji_data(date)
            ret = report_command_one_key_name(json_data, "大吉")
            await client.send_message(message.channel, ret)
            ret = report_command_one_key_eth(json_data, "大吉")
            await client.send_message(message.channel, ret)
        else:
            await client.send_message(message.channel, "指定の年月日のおみくじ情報はありません。")
        

