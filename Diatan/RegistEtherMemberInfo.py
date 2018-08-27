#coding: utf-8
# ver 2.1
import builtins

import re
import json
import types
import base64
import os
import sys
import datetime
import time
import glob
import discord

import WalletAddressDeleter

async def report_error(message, error_msg):
    em = discord.Embed(title=" ", description="─────────\n" + message.author.display_name, color=0xDEED33)
    em.set_author(name='ディア', icon_url=client.user.default_avatar_url)
    em.set_author(name='ディア', icon_url='http://bdacoin.org/bot/omikuji/image/face.png')
    
    em.add_field(name="エラー", value=error_msg, inline=False)
    try:
        print(error_msg)
        await client.send_message(message.channel, embed=em)
    except:
        print(sys.exc_info())

def get_data_memberinfo_path(message, id):
    return 'DataMemberInfo/' + str(id) + ".json"

def get_data_memberpaid_path(message, id):
    return 'DataMemberPaid/' + str(id) + ".json"


async def update_one_member_data(message, address, id):
    try:

        path = get_data_memberinfo_path(message, id)
        print(path)
        with open(path, "r") as fr:
            memberinfo = json.load(fr)

        memberinfo["eth_address"] = address

        path = get_data_memberinfo_path(message, id)
        json_data = json.dumps(memberinfo, indent=4)
        with open(path, "w") as fw:
            fw.write(json_data)
        return True

    except:
        await report_error(message, "MemberDataデータ作成中にエラー")
        await report_error(message, sys.exc_info())
    
    return False

# 1人分のメンバーデータの作成
async def make_one_member_data(message, address, id):
    try:
        memberinfo = {
            "eth_address": "",
            "waves_address": "",
            "omikuji_ticket_count": 0,
            "roulette_ticket_count": 0,
            "food_ticket_count": 0,
            "drink_ticket_count": 0,
            "kaiwa_experiment": 0,
            "kaiwa_experiment_coef": 1,
            "blog_lv": 0,
            "kaiwa_lv": 0,
            "user_id": 0
        }
        
        memberinfo["user_id"] = id

        memberinfo["eth_address"] = address

        memberinfo["omikuji_ticket_count"] = 1
        
        path = get_data_memberinfo_path(message, id)
        print(path)
        json_data = json.dumps(memberinfo, indent=4)
        with open(path, "w") as fw:
            fw.write(json_data)
        return True
    except:
        await report_error(message, "MemberDataデータ作成中にエラーが発生しました。")
        await report_error(message, sys.exc_info())
    return False


async def make_one_member_paid(message, id):
    try:
        paidinfo = {
            "kaiwa_paid_lv": 0,
            "blog_paid_lv": 0,
            "invite_paid_lv": 0,
            "kaiwa_paid_amount": 0,
            "blog_paid_amount": 0,
            "invite_paid_amount": 0,
            "swap_amount": 0,
            "user_id": 0
        }
        
        paidinfo["user_id"] = id
        
        path = get_data_memberpaid_path(message, id)
        print(path)
        json_data = json.dumps(paidinfo, indent=4)
        with open(path, "w") as fw:
            fw.write(json_data)
        return True
    except:
        await report_error(message, "MemberPaidデータ作成中にエラーが発生しました。")
        await report_error(message, sys.exc_info())
    
    return False


async def regist_one_member_data(message, id):

    address = message.content.strip()
    # イーサアドレス登録だ
    if WalletAddressDeleter.is_message_ether_pattern(address):
        try:
            # すでに登録済みである
            path = get_data_memberinfo_path(message, id)
            if (os.path.exists(path)):
                # 何もしない
                await update_one_member_data(message, address, id)
            # 存在しなかった時にやる
            else:
                await make_one_member_data(message, address, id)

            path = get_data_memberpaid_path(message, id)
            if (os.path.exists(path)):
                # 何もしない
                pass
            # 存在しなかった時にやる
            else:
                await make_one_member_paid(message, id)
        except:
            print("regist_one_member_data でエラー")
            print(sys.exc_info())
    else:
        await report_error(message, "イーサアドレスのパターンではありません。")
        return



def is_regist_one_member_data_condition(message):
    if "イーサアドレス登録" in str(message.channel):
        return True

    return False


