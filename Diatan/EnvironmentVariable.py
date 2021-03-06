#coding: utf-8
# ver 2.1

#
# Copyright (C) 2018 Akitsugu Komiyama
# under the GPL v3 License.
# 
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



