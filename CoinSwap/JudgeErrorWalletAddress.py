#coding: utf-8
# ver 2.1

# 正規表現
import re
import asyncio

# Wavesアドレスはダメなチャンネル
nopermit_channnel_of_waves_address = ["^交換受付窓口.+$"]

# Etherアドレスはダメなチャンネル
nopermit_channnel_of_ether_address = ["^交換受付窓口.+$"]


# Wavesウォレットのアドレスのパターン
def is_message_waves_pattern(message):
    message = message.strip();
    if len(message) != 35:
        return False

    if re.match("^(\s*)3P[0-9a-zA-Z]+(\s*)$", message):
        return True
    
    return False
    
# Etherウォレットのアドレスのパターン
def is_message_ether_pattern(message):
    message = message.strip();
    if len(message) != 42:
        return False

    if re.match("^(\s*)0x[0-9a-zA-Z]+(\s*)$", message):
        return True
    
    return False


def is_nopermit_waves_channel(channel_name):
    cn_name = str(channel_name)
    # wavesアドレスが許されないチャンネルのいずれかか？
    for pattern in nopermit_channnel_of_waves_address:
        if re.match(pattern, cn_name):
            return True

    return False

def is_nopermit_ether_channel(channel_name):
    cn_name = str(channel_name)
    # etherアドレスが許されないチャンネルのいずれかか？
    for pattern in nopermit_channnel_of_ether_address:
        if re.match(pattern, cn_name):
            return True

    return False


async def error_wallet_address_message(message):

    is_error = False

    if is_nopermit_waves_channel(message.channel):
        if is_message_waves_pattern(message.content):
            is_error = True
            await client.send_message(message.channel, "Waves Address ではなく、Waves Transaction ID を投稿してください。")

    if is_nopermit_ether_channel(message.channel):
        if is_message_ether_pattern(message.content):
            is_error = True
            await client.send_message(message.channel, "Ether Address ではなく、Waves Transaction ID を投稿してください。")
            
    return is_error
