#coding: utf-8
# ver 2.1
import os


def get_discord_bot_token():
    # テスト用が有効ならテストサーバー用の接続トークンを返す
    BOT_TOKEN = os.getenv("DISCORD_TEST_BOT_TOKEN", r'')
    if BOT_TOKEN != "-":
        return BOT_TOKEN

    # 本番用のみが有効なら本番用の接続トークンを返す
    BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", r'')
    if BOT_TOKEN != "":
        return BOT_TOKEN

    print("エラー: 環境変数のDISCORD_BOT_TOKENが設定されていない")
    return None



def get_docomo_naturalchat_key():
    KEY = os.getenv("DISCORD_DOCOMO_NATURALCHAT_KEY", r'')
    appid_01 = os.getenv("DISCORD_DOCOMO_NATURALCHAT_APPID_01", r'')
    appid_02 = os.getenv("DISCORD_DOCOMO_NATURALCHAT_APPID_02", r'')
    appid_03 = os.getenv("DISCORD_DOCOMO_NATURALCHAT_APPID_03", r'')
    return {"KEY":KEY, "appid_01":appid_01, "appid_02":appid_02, "appid_03":appid_03}
