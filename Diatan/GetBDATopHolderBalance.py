import requests
import sys
import re
import os
import json

def get_bdr_top_holders_html(p):
    try:
        res = requests.get('https://etherscan.io/token/generic-tokenholders2?a=0xf6caa4bebd8fab8489bc4708344d9634315c4340&s=0&p=1')
        res.raise_for_status()
        return res.text
    except:
        return None



def get_all_member_id_and_ether_bind_data():
    dict_data = {}
    dirlist = os.listdir("./DataMemberInfo")
    # print(dirlist)
    for j in dirlist:
        path = "./DataMemberInfo/" + j
        try:
            with open(path, "r") as fr:
                memberinfo = json.load(fr)
                m_add = memberinfo["eth_address"].lower()
                m_id = memberinfo["user_id"]
                dict_data[m_add] = m_id
        except:
            print("Error")
            pass
    
    return dict_data

async def add_level_role(roles, author, level):
    # そのサーバーが持ってる役職
    roles_list = roles
    for r in roles_list:
        try:
            #print(r.name)
            # 役職の名前そのものに必須到達レベルがある。
            m = re.search(".+\s*LV(\d+)", r.name, re.IGNORECASE)
            if m:
                #print("マッチ" + r.name)
                roles_lv = m.group(1)
                if roles_lv and int(roles_lv) <= level:
                    # print("付与開始" + r.name)
                    await client.add_roles(author, r)
                    print("付与した" + r.name)
        except Exception as e:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))

def aaa():
    html = get_bdr_top_holders_html(1)
    # print(html)
    ret_list = re.findall("<tr><td>\d+</td><td><span><a href='/token/0xf6caa4bebd8fab8489bc4708344d9634315c4340\?a=(0x.+?)' target='_parent'>0x.+?</a></span></td><td>(\d+)</td><td>\d+%</td></tr>", html)
    # イーサアドレスを小文字に統一する
    for ix in range(0, len(ret_list)):
        ret_list[ix] = [ret_list[ix][0], ret_list[ix][1].lower()]
    
    # イーサアドレス(小文字)がキー、値がユーザーIDの辞書を取得
    dict_data = get_all_member_id_and_ether_bind_data()
    
    # ホルダー一覧で
    for holder in ret_list:
        # イーサアドレス(小文字)
        eadd = holder[0]
        # ホールド量
        amount = holder[1]
        try:
            # イーサアドレスに紐づいたユーザーIDがあるなら
            if eadd in dict_data:
                print( str(dict_data[eadd]) + ":" + amount)
        except:
            pass
    # print(ret_list)





if __name__ == '__main__':
