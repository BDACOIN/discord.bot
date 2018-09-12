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

import EnvironmentVariable
import WalletAddressDeleter
import JapaneseOmikuji
import MicMessage
import NaturalChat

import RegistEtherMemberInfo
import EastAsianWidthCounter
import ImageCategory
import AirdropMemberInfo
import copy

import ChatLevelUp

# 上記で取得したアプリのトークンを入力



# テストサーバー用のトークン
BOT_TOKEN = EnvironmentVariable.get_discord_bot_token()



# パッケージのインポートとインスタンス作成
client = discord.Client()

# 他のモジュールへの伝搬が面倒なので、Pythonの組み込み変数同様の扱いにしてしまう
builtins.client = client

ChatLevelUp.createChatLevelUpTable()

# ログイン&準備が完了したら一度だけ実行される
@client.event
async def on_ready():
    # コンソールにBOTとしてログインした名前とUSER-IDを出力
    print('Logged in as')
    print('BOT-NAME :', client.user.name)
    print('BOT-ID   :', client.user.id)
    print('------')



sm1, sm2, sm3, sm4 = NaturalChat.CreateObject()
print(sm1)
print(sm3)
print(sm3)
print(sm4)

builtins.sm4 = sm4

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

    # 許可されないWalletアドレスのメッセージ
    is_delete = await WalletAddressDeleter.violation_wallet_address_message(message)
    if is_delete:
        return

    # メンバー情報の表示
    if RegistEtherMemberInfo.is_show_one_member_data_condition(message):
        await RegistEtherMemberInfo.show_one_member_data(message, message.author.id)
        return

    # イーサアドレスの登録
    if RegistEtherMemberInfo.is_regist_one_member_data_condition(message):
        await RegistEtherMemberInfo.regist_one_member_data(message, message.author.id)
        return

    # メンバー情報の表示
    if AirdropMemberInfo.is_show_one_member_data_condition(message):
        await AirdropMemberInfo.show_one_member_data(message, message.author.id)
        return


    # エアドロのイーサアドレスの登録
    if AirdropMemberInfo.is_regist_one_member_data_condition(message):
        await AirdropMemberInfo.regist_one_member_data(message, message.author.id)
        return

    # ディアたんのマイクの処理
    if MicMessage.is_mic_permission_condition(message):
        await MicMessage.say_message(message)
        return

    # おみくじの集計結果
    if JapaneseOmikuji.is_report_command_condition(message.content):
        await JapaneseOmikuji.report_command(message)
        return

    try:
        if ChatLevelUp.is_level_command_condition(message.content):
            await ChatLevelUp.command_show_level_infomation(message)
            return
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))


    # イメージカテゴリ
    try:
        att = ImageCategory.is_analyze_condition(message)
        if att != None:
            await ImageCategory.analyze_image(message, att)
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
        print("例外:is_analyze_condition")
        pass


    # 表示
    if len(message.content) > 0:
        for regex in NaturalChat.NaturalChattableChannelRegex():
            if re.match(regex, str(message.channel)):
            
                if str(message.channel) == "雑談":

                    try:
                        msg = str(message.content)
                        dia_appear_remain_cnt = sm3.decrement_appear_zatsudan_cnt(msg)
                        if dia_appear_remain_cnt >= 0:
                            # 3の方を使って会話
                            msg = sm3.get_naturalchat_mesasge(message)
                            await client.send_message(message.channel, msg)

                    except RuntimeError:
                        print(RuntimeError)


                # おみくじが許される条件
                elif JapaneseOmikuji.is_permission_omikuji_condition(message):
                    # 2の方を使って会話
                    msg = sm2.get_naturalchat_mesasge(message)
                    await client.send_message(message.channel, msg)
                    await JapaneseOmikuji.say_embedded_omikuji_message(message)

                else:
                    # 1の方を使って会話
                    msg = sm1.get_naturalchat_mesasge(message)
                    await client.send_message(message.channel, msg)
    
    # 会話からおみくじを得る
    try:
        await JapaneseOmikuji.get_omikuji_from_kaiwa(message)
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
        print("例外:get_omikuji_from_kaiwa")
        pass

    try:
        await ChatLevelUp.push_kaiwa_post(message, message.content)
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
        print(sys.exc_info())
        
    if message.author.id == "397238348877529099":
        if message.content == "!all_level_roles":
            await ChatLevelUp.all_member_add_level_role(message)
            


def get_welcome_channel(member):
    for ch in member.server.channels:
        if "welcome" == str(ch):
            return ch
            
    return None


def get_data_inviteinfo_path():
    return "DataInviteInfo/InviteInfo.json"

# https://foolean.net/p/1691

@client.event
async def on_member_join(member):
    print("on_member_join")

    path = get_data_inviteinfo_path()
    with open(path, "r") as fr:
        inviteinfo = json.load(fr)

    this_member_inviter = 0

    # サーバーにある招待オブジェクトリスト
    invites = await client.invites_from(member.server)
    # print(invites)
    for invite in invites:

        # 招待状の期限が無限でないものは考慮外
        if invite.max_age != 0:
            continue

        print(invite)

        # すでに存在するが、
        if not invite.id in inviteinfo:
            # 追加
            inviteinfo[invite.id] = {"uses":invite.uses, "owner":_inviter.id, "children":[]}

        # 前回の使用者数と食い違っている
        
        invitehash = inviteinfo[invite.id]
        print("invite.uses" + str(invite.uses))
        print("invitehash['uses']" + str(invitehash["uses"]))
        if invite.uses != invitehash["uses"]:

            _inviter = invite.inviter

            print("これが使われた" + _inviter.id + ":" + _inviter.name)
            if not "children" in invitehash:
                invitehash["children"] = []
            
            # メンバーIDがまだそこに追加されてなければ
            if not member.id in invitehash["children"]:
                # このメンバーが、招待された人としてIDを追加する
                invitehash["children"].append(member.id)
                this_member_inviter = _inviter
                break


    path = get_data_inviteinfo_path()
    json_data = json.dumps(inviteinfo, indent=4)
    with open(path, "w") as fw:
        print("保存した")
        fw.write(json_data)

    ch = get_welcome_channel(member)
    await client.send_message(ch, "新規参加者の識別ID:" + member.id +":"+ "<@"+member.id +">")
    if this_member_inviter != 0:
        await client.send_message(ch, "この人を招待した人" + "<@"+this_member_inviter.id +">")


@client.event
async def on_member_remove(member):

    path = get_data_inviteinfo_path()
    with open(path, "r") as fr:
        inviteinfo = json.load(fr)

    this_member_inviter = 0
        
    # その中をなめまわして、該当のメンバーがいるなら削除
    for key in inviteinfo:
        invitehash = inviteinfo[key]
        if not "children" in invitehash:
            invitehash["children"] = []
    
        # メンバーIDが配列にあるならば
        if member.id in invitehash["children"]:
            # このメンバーが、招待された人としてIDを追加する
            invitehash["children"].remove(member.id)
            try:
                _user = await client.get_user_info(invitehash["owner"])
                print("招待者のユーザーオブジェクト:" + str(_user))
                this_member_inviter = _user
            except Exception as e:
                t, v, tb = sys.exc_info()
                print(traceback.format_exception(t,v,tb))
                print(traceback.format_tb(e.__traceback__))
                pass


    # サーバーにある招待オブジェクトリスト
    invites = await client.invites_from(member.server)
    # print(invites)
    for invite in invites:
        # 招待状の期限が無限でないものは考慮外
        if invite.max_age != 0:
            continue

        print(invite)
        _inviter = invite.inviter

        # すでに存在するが、
        if not invite.id in inviteinfo:
            # 追加
            inviteinfo[invite.id] = {"uses":invite.uses, "owner":_inviter.id, "children":[]}
        else:
            # カウント数を最新に
            inviteinfo[invite.id]["uses"] = invite.uses
        
    path = get_data_inviteinfo_path()
    json_data = json.dumps(inviteinfo, indent=4)
    with open(path, "w") as fw:
        print("保存した")
        fw.write(json_data)

    ch = get_welcome_channel(member)
    await client.send_message(ch, "退場者の識別ID:" + member.id +":"+ "<@"+member.id +">")
    if this_member_inviter != 0:
        await client.send_message(ch, "この人を招待した人" + "<@"+this_member_inviter.id +">")
            
# APP(BOT)を実行
client.run(BOT_TOKEN)
