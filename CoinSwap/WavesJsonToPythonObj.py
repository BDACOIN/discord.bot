import json
import math
import Base58DecodedWalletAddress
import JudgeErrorWalletAddress

asset_id_of_BDA = "ANdLVFpTmpxPsCwMZq7hHMfikSVz8LBZNykziPgnZ7sn" # BLACK DIA WAVESトークンのAssetID。これは固定

recipient_wallet_address_of_BDA = "3P7DGDmNEdCgN5XM7Qenxk8K8jGrTLHjRRQ" # 受け取り申請先のウォレットアドレス。まだ実験用

def json_to_python_obj(str_json):

    json_obj = json.loads(str_json)

    if "status" in json_obj and json_obj["status"] == "error":
        # print("error")
        return {"status":"error", "details":"対象のデータはトランザクションデータではありません。" }

    # assetidが無い。おそらくはwaves本体コインか何かの送信データ
    if not "assetId" in json_obj:
        return {"status":"error", "asset_error":True, "details":"対象のデータはBDA(Waves版)のトランザクションデータではありません。" }

    # assetはあるが、BDAのものではない。
    if json_obj["assetId"] != asset_id_of_BDA:
        return {"status":"error", "asset_error":True, "details":"対象のデータはBDA(Waves版)のトランザクションデータではありません。" }


    # 送金先（受信者）のウォレットアドレス
    recipient = ""

    # 送金者が普通に単発送金してる時
    if "recipient" in json_obj:
        recipient = json_obj["recipient"]
        amount = json_obj["amount"]

    # 送金者が一斉送金している時。transfersを見てネスト情報を見る、受信アドレスが等しいやつだけ足していく
    elif "transfers" in json_obj:
        transfers = json_obj["transfers"]
        amount = 0
        for tr in transfers:
            if tr["recipient"] == recipient_wallet_address_of_BDA:
                recipient = tr["recipient"]
                amount = amount + tr["amount"]

        amount = amount

    # 受信アドレスが等しくないならば、ここで終わり
    if recipient != recipient_wallet_address_of_BDA:
        return {"status":"error", "details":"送金先のWavesウォレットアドレスが、BDA指定のものと異なります。" }

    # 一応トランザクションID自体も控えておく
    transaction_id = json_obj["id"]

    # 受信アドレスが等しければ続きの情報を拾う
    # 送信主のアドレス
    sender = json_obj["sender"]

    # タイムスタンプ
    timestamp = json_obj["timestamp"]

    # wavesノード上に出てるのは、10倍なので、1/10する。(よくわからないが、BDA waves版が「decimal 1」での発行と思われる)
    amount = amount / 10.0
    # イーサートークン比率は比率は25:1
    eth_amount = amount / 25.0
    # 最後にintで丸める。切り捨て。ガス代等を考慮
    eth_amount = int(eth_amount)

    # アタッチメントにイーサーウォレットのアドレスがあるはず
    attachment = json_obj["attachment"]

    # アタッチメントは、原文のままになる場合と、base58エンコードがかかる場合がある。
    try:
        # base58デコードした文字列を返す。失敗した場合原文文字列ままを返す。
        attachment = Base58DecodedWalletAddress.get_base58_decoded_wallet_address(attachment)
    except:
        attachment = ""
        # print("送金先イーサーアドレスエラー")

    attachment = attachment.strip()
    eth_address_and_user_id = attachment.split(",")
    # ユーザーIDを設定し忘れている
    if len(eth_address_and_user_id) == 1:
        user_id = 0 # とりあえず仕方が無いので0
        eth_address = eth_address_and_user_id[0]
        eth_address = eth_address.strip()
    elif len(eth_address_and_user_id) >= 2:
        try:
            eth_address = eth_address_and_user_id[0]
            # 掃除
            eth_address = eth_address.strip()

            str_user_id = eth_address_and_user_id[1]
            # 掃除
            str_user_id = str_user_id.strip()
            # 数字を数値とする
            user_id = int(str_user_id)
        except:
            user_id = 0 # とりあえず仕方が無いので0
    else:
        eth_address = attachment


    # print(sender)
    # print(amount)
    # print(eth_amount)
    # print(transaction_id)
    # print(attachment)

    # 基本情報をセッティング
    rtn_dict = {
        "transaction_id":transaction_id,
        "sender":sender,
        "amount":amount,
        "timestamp":timestamp,
        "eth_address":eth_address,
        "eth_amount":eth_amount,
        "attachment":attachment,
        "user_id":user_id
    }

    # 送金者が、Attachmentに記載した情報が、イーサーアドレスとして不適切なことが明白であれば…
    # エラー情報を付加情報として記載しておく。
    # 送金自体はしてしまってるので特別な対処が必要かもしれない。
    if JudgeErrorWalletAddress.is_message_ether_pattern(eth_address) != True:
        rtn_dict["eth_status"] = "error"
        rtn_dict["eth_status_details"] = "送金先のイーサーアドレスが不正です。"

    if user_id == 0:
        rtn_dict["user_id_status"] = "error"
        rtn_dict["user_id_status_details"] = "ユーザーIDが不正です。"


    return rtn_dict





# テスト
if __name__ == '__main__':
    # 正常
    test_json1 = r"""{
    "type" : 4,
    "id" : "3qDqKc16QK1owMSFhwjBPH5jrhErSNWn2kVHiL9qrFLV",
    "sender" : "3PMahF2qDnkEZbCHC7dznUVBrfDqctGyEom",
    "senderPublicKey" : "EUpjLEaJoaM2wR6QEP5FcSfCT59EUDGVsVsRgirsvUDs",
    "fee" : 100000,
    "timestamp" : 1526095564397,
    "signature" : "5j4rUmR5nptYDQLEBY7rJ6SR2UEvdQEPF8AhjPmhBqpFY1nPNykgBmTwvnweSA2mnQ6waLhm9GwnHzp5jt1H484m",
    "version" : 1,
    "recipient" : "3PFCT4q6K56zC8YGa8vBaXgvkfFvJnRdFF8",
    "assetId" : "ANdLVFpTmpxPsCwMZq7hHMfikSVz8LBZNykziPgnZ7sn",
    "feeAssetId" : null,
    "feeAsset" : null,
    "amount" : 1500000,
    "attachment" : "ovFJPq8LJzj6zhiULUCHzsJD9DVrw3hUA54qWbbXMbGsLvfmkiFCp62WR",
    "height" : 996705
    }"""

    # そもそも変
    test_json2 = r'{ "status":"error", "details":"Transaction is not in blockchain" }'

    # 正常だが一斉送信のなかに、BDAへの送金が含まれてる。
    test_json3 = r"""{
    "type" : 11,
    "id" : "J9Py9czWYSnp7wBxESuCHku4G78n73z4Utn3xsuTLAEc",
    "sender" : "3PM2LPgW8FjCsZDBivZ8gdVrYnJMM1vPQNx",
    "senderPublicKey" : "XXv5HCMKjjmEiqstGwZDnrRbg5pT1f29k4kQWyMaNms",
    "fee" : 150000,
    "timestamp" : 1531139477097,
    "proofs" : [ "2ARQqqCVifv3vYJbfnFWZQ16ZYKcvoqYySv4AyVVJS6DhhVVXwpQT2ga3vqFVQFEy29BfmprPdKHFg21QosbPHoH" ],
    "version" : 1,
    "assetId" : "ANdLVFpTmpxPsCwMZq7hHMfikSVz8LBZNykziPgnZ7sn",
    "attachment" : "ovFJPq8LJzj6zhiULUCHzsJD9DVrw3hUA54qWbbXMbGsLvfmkiFCp62WR",
    "transferCount" : 1,
    "totalAmount" : 200000,
    "transfers" : [ {
        "recipient" : "3PFCT4q6K56zC8YGa8vBaXgvkfFvJnRdFF8",
        "amount" : 200000
    }, {
        "recipient" : "3PFCT4q6K56zC8YGa8vBaXgvkfFvJnRdFF8",
        "amount" : 700000
    }, {
        "recipient" : "3PFCT4q6K56zC8YGa8vBaXgvkfFvJnRd555",
        "amount" : 300000
    } ],
    "height" : 1075581
    }"""

    # アタッチメント忘れ
    test_json4 = r"""{
    "type" : 4,
    "id" : "3qDqKc16QK1owMSFhwjBPH5jrhErSNWn2kVHiL9qrFLV",
    "sender" : "3PMahF2qDnkEZbCHC7dznUVBrfDqctGyEom",
    "senderPublicKey" : "EUpjLEaJoaM2wR6QEP5FcSfCT59EUDGVsVsRgirsvUDs",
    "fee" : 100000,
    "timestamp" : 1526095564397,
    "signature" : "5j4rUmR5nptYDQLEBY7rJ6SR2UEvdQEPF8AhjPmhBqpFY1nPNykgBmTwvnweSA2mnQ6waLhm9GwnHzp5jt1H484m",
    "version" : 1,
    "recipient" : "3PFCT4q6K56zC8YGa8vBaXgvkfFvJnRdFF8",
    "assetId" : "ANdLVFpTmpxPsCwMZq7hHMfikSVz8LBZNykziPgnZ7sn",
    "feeAssetId" : null,
    "feeAsset" : null,
    "amount" : 1500000,
    "attachment" : "",
    "height" : 996705
    }"""

    # 受信アドレスとしてBDAの指定ウォレットが含まれてない
    test_json5 = r"""{
    "type" : 4,
    "id" : "3qDqKc16QK1owMSFhwjBPH5jrhErSNWn2kVHiL9qrFLV",
    "sender" : "3PMahF2qDnkEZbCHC7dznUVBrfDqctGyEom",
    "senderPublicKey" : "EUpjLEaJoaM2wR6QEP5FcSfCT59EUDGVsVsRgirsvUDs",
    "fee" : 100000,
    "timestamp" : 1526095564397,
    "signature" : "5j4rUmR5nptYDQLEBY7rJ6SR2UEvdQEPF8AhjPmhBqpFY1nPNykgBmTwvnweSA2mnQ6waLhm9GwnHzp5jt1H484m",
    "version" : 1,
    "recipient" : "3PFCT4q6K56zC8YGa8vBaXgvkf888888888",
    "assetId" : "ANdLVFpTmpxPsCwMZq7hHMfikSVz8LBZNykziPgnZ7sn",
    "feeAssetId" : null,
    "feeAsset" : null,
    "amount" : 1500000,
    "attachment" : "",
    "height" : 996705
    }"""

    # 一斉送信だが、そのなかに１つも受信アドレスとしてBDAの指定ウォレットが含まれてない。
    test_json6 = r"""{
    "type" : 11,
    "id" : "J9Py9czWYSnp7wBxESuCHku4G78n73z4Utn3xsuTLAEc",
    "sender" : "3PM2LPgW8FjCsZDBivZ8gdVrYnJMM1vPQNx",
    "senderPublicKey" : "XXv5HCMKjjmEiqstGwZDnrRbg5pT1f29k4kQWyMaNms",
    "fee" : 150000,
    "timestamp" : 1531139477097,
    "proofs" : [ "2ARQqqCVifv3vYJbfnFWZQ16ZYKcvoqYySv4AyVVJS6DhhVVXwpQT2ga3vqFVQFEy29BfmprPdKHFg21QosbPHoH" ],
    "version" : 1,
    "assetId" : "ANdLVFpTmpxPsCwMZq7hHMfikSVz8LBZNykziPgnZ7sn",
    "attachment" : "ovFJPq8LJzj6zhiULUCHzsJD9DVrw3hUA54qWbbXMbGsLvfmkiFCp62WR",
    "transferCount" : 1,
    "totalAmount" : 200000,
    "transfers" : [ {
        "recipient" : "3PFCT4q6K56zC8YGa8vBaXgvkfFvJnRd555",
        "amount" : 200000
    }, {
        "recipient" : "3PFCT4q6K56zC8YGa8vBaXgvkfFvJnRd555",
        "amount" : 700000
    }, {
        "recipient" : "3PFCT4q6K56zC8YGa8vBaXgvkfFvJnRd555",
        "amount" : 300000
    } ],
    "height" : 1075581
    }"""

    # アタッチメントしてるがイーサアドレスではない。
    test_json6 = r"""{
    "type" : 4,
    "id" : "3qDqKc16QK1owMSFhwjBPH5jrhErSNWn2kVHiL9qrFLV",
    "sender" : "3PMahF2qDnkEZbCHC7dznUVBrfDqctGyEom",
    "senderPublicKey" : "EUpjLEaJoaM2wR6QEP5FcSfCT59EUDGVsVsRgirsvUDs",
    "fee" : 100000,
    "timestamp" : 1526095564397,
    "signature" : "5j4rUmR5nptYDQLEBY7rJ6SR2UEvdQEPF8AhjPmhBqpFY1nPNykgBmTwvnweSA2mnQ6waLhm9GwnHzp5jt1H484m",
    "version" : 1,
    "recipient" : "3PFCT4q6K56zC8YGa8vBaXgvkfFvJnRdFF8",
    "assetId" : "ANdLVFpTmpxPsCwMZq7hHMfikSVz8LBZNykziPgnZ7sn",
    "feeAssetId" : null,
    "feeAsset" : null,
    "amount" : 1500000,
    "attachment" : "0x494Da578D0470A2E43B8668826De87e6BC74bECf です、よろしくお願いします。",
    "height" : 996705
    }"""


    for t in (test_json1, test_json2, test_json3, test_json4, test_json5, test_json6):
        test_pyobj = json_to_python_obj(t)
        print(test_pyobj)
        print("-------------------------------------------------------")