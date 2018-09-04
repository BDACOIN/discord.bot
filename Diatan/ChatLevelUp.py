# -*- coding: utf-8 -*-

import unicodedata
import difflib

import builtins

import re
import json
import os
import sys, datetime, time
import discord

import EastAsianWidthCounter

# そのレベルになるのに必要な総経験値(Mee6と同じ計算式)
def need_experiment_value(level):
    xp_to_desired_level = 5 / 6 * level * (2 * level * level + 27 * level + 91);
    return xp_to_desired_level


LV_TO_EXP_LIST = []
def createChatLevelUpTable():
    if len(LV_TO_EXP_LIST) ==0:
        # lv200まで埋める
        for lv in range(0, 201):
            LV_TO_EXP_LIST.append([lv, need_experiment_value(lv)])

    print(LV_TO_EXP_LIST)


def get_lv_from_exp(exp):
    lv = 0
    for t in LV_TO_EXP_LIST:
        # 指定された経験値より、レベル表の総合経験値が低いなら
        if t[1] < exp:
            lv = t[0] # すくなくともそのレベルには到達している
    
    return lv

# ２つのテキストの類似度の比較
def get_sequence_matcher_coef(test_1, text_2):

    # unicodedata.normalize() で全角英数字や半角カタカナなどを正規化する
    normalized_str1 = unicodedata.normalize('NFKC', test_1)
    normalized_str2 = unicodedata.normalize('NFKC', text_2)

    # 類似度を計算、0.0~1.0 で結果が返る
    s = difflib.SequenceMatcher(None, normalized_str1, normalized_str2).ratio()
    # print( "match ratio:" + str(s))
    return s


async def report_error(message, error_msg):
    print(message, error_msg)
    em = discord.Embed(title=" ", description="─────────\n" , color=0xDEED33)
    em.set_author(name='ディア', icon_url=client.user.default_avatar_url)
    em.set_author(name='ディア', icon_url='http://bdacoin.org/bot/omikuji/image/face.png')
    
    em.add_field(name="返信相手", value= "<@" + message.author.id + ">", inline=False)
    em.add_field(name="エラー", value=error_msg, inline=False)
    try:
        print(error_msg)
        await client.send_message(message.channel, embed=em)
    except:
        print(sys.exc_info())


def get_data_kaiwa_post_path(message):
    id = message.author.id
    return 'DataMemberPostInfo/' + str(id) + ".json"


def has_post_data(message):
    path = get_data_kaiwa_post_path(message)
    if not os.path.exists(path):
        return False
    else:
        return True


    


async def is_syougou_up(message):
    pass


async def update_one_kaiwa_post_data(message):
    try:
        if not has_post_data(message):
            await make_one_kaiwa_post_data(message)

        path = get_data_kaiwa_post_path(message)
        print(path)
        with open(path, "r") as fr:
            postinfo = json.load(fr)

        # まずは履歴として加える
        text = message.content.strip()

        # 経験値の加算係数を出す
        minimum_coef = 1
        # 過去の20投稿との比較で最低の係数を出す（類似したものがあるほど係数が低くなる)
        for hist in postinfo["posthistory"]:
            temp_coef = 1 - get_sequence_matcher_coef(hist, text)
            print("どうか:" + str(temp_coef) + hist + ", " + text)
            if temp_coef < minimum_coef:
                minimum_coef = temp_coef

        print("最低係数:" + str(minimum_coef))

        base_experience = 40
        add_experience = int(minimum_coef * base_experience)
        if add_experience <= 0:
            add_experience = 1
        postinfo["exp"] = postinfo["exp"] + add_experience
        print(str(add_experience) + "が経験値として加算された")
        
        # テキストも履歴として加える
        postinfo["posthistory"].append(text)

        # 多くなりすぎていれば削除。
        # 3回ぐらい繰り返しておけば十分か
        for rng in [0, 1, 2]:
            # すでに履歴が10以上あれば
            if len(postinfo["posthistory"]) > 10:
                # 先頭をカット
                postinfo["posthistory"].pop(0)


        print("ただいまのレベル" + str(get_lv_from_exp(postinfo["exp"])))

        path = get_data_kaiwa_post_path(message)
        json_data = json.dumps(postinfo, indent=4)
        with open(path, "w") as fw:
            fw.write(json_data)
            
        return postinfo

    except:
        await report_error(message, "update_one_kaiwa_post_dataデータ作成中にエラー")
        await report_error(message, sys.exc_info())
    
    return None


# 1人分のメンバーデータの作成
async def make_one_kaiwa_post_data(message):
    try:
        postinfo = {
            "id": message.author.id,
            "posthistory": [],
            "exp": 0,
        }
        
        path = get_data_kaiwa_post_path(message)
        print("ここきた★" + path)
        json_data = json.dumps(postinfo, indent=4)
        with open(path, "w") as fw:
            fw.write(json_data)
        return postinfo
    except:
        await report_error(message, "make_one_kaiwa_post_data 中にエラーが発生しました。")
        await report_error(message, sys.exc_info())
    return None


async def load_one_kaiwa_data(message):
    try:
        if not has_post_data(message):
            await make_one_kaiwa_post_data(message)
    
        with open(path, "r") as fr:
            postinfo = json.load(fr)

        path = get_data_kaiwa_post_path(message)
        print(path)
        with open(path, "r") as fr:
            postinfo = json.load(fr)


        return postinfo

    except:
        await report_error(message, "load_one_kaiwa_data 中にエラー")
        await report_error(message, sys.exc_info())
    
    return None


async def push_kaiwa_post(message, text):

    postinfo = await update_one_kaiwa_post_data(message)
    if postinfo != None:
        is_level_up(message)
        is_shougou_up(message)
    
    # count = EastAsianWidthCounter.get_east_asian_width_count_effort(text)
    print(count)

# テスト
if __name__ == '__main__':
    mesage = {"content": "スパスパゲッティ", "id": 3333333333}
    push_kaiwa_post(mesage, "")
    push_kaiwa_post(mesage, "aaaaaa")


