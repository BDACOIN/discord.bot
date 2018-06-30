#coding: utf-8
# ver 2.0


import random
import discord


def is_permission_omikuji_condition(message):
    ch = str(message.channel)
    if ch in ["★おみくじコーナー★"]:
       return True
    if ch in ["ディアたんと会話"] and (random.randint(1,10) < 3):
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



def get_embedded_omikuji_object(message):

    un_list = [
        ["大吉","01"],
        ["吉","02"],
        ["中吉","03"],
        ["末吉","04"],
        ["凶","05"]
    ]

    # １つランダムで選ぶ
    target = random.choice(un_list)

    # 
    em = discord.Embed(title=" ", description="─────────\n" + message.author.display_name + " さんの運勢は ...", color=0xDEED33)
#    em = discord.Embed(title=message.author.display_name + " さんの運勢", description=message.author.display_name + " さんの運勢は... __" + target[0] + "__ですよ!!", colour=0xDEED33)
    em.set_author(name='ディア', icon_url=client.user.default_avatar_url)
    em.set_author(name='ディア', icon_url='http://bdacoin.org/bot/omikuji/image/face.png')
    
    em.add_field(name=target[0] + "です!!", value="─────────", inline=False)
    
    em.set_thumbnail(url="http://bdacoin.org/bot/omikuji/image/" + target[1] + "_omkj.png")

    em.set_image(url="http://bdacoin.org/bot/omikuji/image/" + target[1] + ".png")
    return em



async def say_embedded_omikuji_message(message):
    if is_omikuji_command(message.content):
        em = get_embedded_omikuji_object(message)
        await client.send_message(message.channel, embed=em)

        # 簡易だと以下だがデザイン性には欠ける
        # await client.send_message(message.channel, str(message.author.display_name) + "さんの運勢だよ!")
        # img_list = [ "01.png", "02.png", "03.png", "04.png", "05.png" ]

        # １つランダムで選ぶ
        # path = random.choice(img_list)

        # 該当チャンネルに投稿する
        # await client.send_file(message.channel, path)
