#
# Copyright (C) 2018 Akitsugu Komiyama
# under the GPL v3 License.
# 

import sys
import base58

def get_base58_decoded_wallet_address(str_attachment):
    try:
        d58 = base58.b58decode(str_attachment)
        uni = d58.decode("utf8")
        return uni
    except:
        return str_attachment

    return uni