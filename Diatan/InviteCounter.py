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
import copy


def get_welcome_count_channel(member):
    for ch in member.server.channels:
        if "招待カウント閲覧" == str(ch):
            return ch
            
    return None

def get_welcome_channel(member):
    for ch in member.server.channels:
        if "welcome" == str(ch):
            return ch
            
    return None


def get_data_inviteinfo_path():
    return "DataInviteInfo/InviteInfo.json"

# https://foolean.net/p/1691


async def on_member_join(member):
    print("on_member_join")

    try:
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

            # print(invite)

            # すでに存在するが、
            if not invite.id in inviteinfo:
                # 追加
                inviteinfo[invite.id] = {"uses":invite.uses, "owner":invite.inviter.id, "children":[]}

            # 前回の使用者数と食い違っている
            
            invitehash = inviteinfo[invite.id]
            # print("invite.uses" + str(invite.uses))
            # print("invitehash['uses']" + str(invitehash["uses"]))
            if invite.uses != invitehash["uses"]:

                _inviter = invite.inviter

                # print("これが使われた" + _inviter.id + ":" + _inviter.name)
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
            fw.write(json_data)

        ch = get_welcome_count_channel(member)
        msg_content = "新規参加者の識別ID:" + member.id +":"+ "<@"+member.id +">\n"
        if this_member_inviter != 0:
            msg_content = msg_content + "└この人を招待した人:" + "<@"+this_member_inviter.id +">" + "\n"

        await client.send_message(ch, msg_content)

        ch2 = get_welcome_channel(member)
        msg_content = "新規参加者:" + member.name + "\n"
        if this_member_inviter != 0:
            msg_content = msg_content + "└この人を招待した人:" + this_member_inviter.name + "\n"

        await client.send_message(ch2, msg_content)

    except:
        pass


async def on_member_remove(member):

    try:
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
                    # print("招待者のユーザーオブジェクト:" + str(_user))
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

            # print(invite)
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
            # print("保存した")
            fw.write(json_data)

        ch = get_welcome_count_channel(member)
        msg_content = "退場者の識別ID:" + member.id +":"+ "<@"+member.id +">\n"
        if this_member_inviter != 0:
            msg_content = msg_content + "└この人を招待した人" + "<@"+this_member_inviter.id +">" + "\n"

        await client.send_message(ch, msg_content)

        ch2 = get_welcome_channel(member)
        msg_content = "退場者:" + member.name + "\n"
        if this_member_inviter != 0:
            msg_content = msg_content + "└この人を招待した人:" + this_member_inviter.name + "\n"

        await client.send_message(ch2, msg_content)

    except:
        pass
            
