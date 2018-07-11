import json
import Base58DecodedWalletAddress
import JudgeErrorWalletAddress

recipient_wallet_address_of_BDA = "3PFCT4q6K56zC8YGa8vBaXgvkfFvJnRdFF8"


def json_to_python_obj(str_json):

    json_obj = json.loads(str_json)

    if "status" in json_obj and json_obj["status"] == "error":
        # print("error")
        return {"status":"error", "details":"対象のデータはトランザクションデータではありません。" }

    # 送金先（受信者）のウォレットアドレス
    recipient = ""

    # 送金者が普通に単発送金してる時
    if "recipient" in json_obj:
        recipient = json_obj["recipient"]
        amount = json_obj["amount"] / 10.0

    # 送金者が一斉送金している時。transfersを見てネスト情報を見る、受信アドレスが等しいやつだけ足していく
    elif "transfers" in json_obj:
        transfers = json_obj["transfers"]
        amount = 0
        for tr in transfers:
            if tr["recipient"] == recipient_wallet_address_of_BDA:
                recipient = tr["recipient"]
                amount = amount + tr["amount"]

        amount = amount / 10.0

    # 受信アドレスが等しくないならば、ここで終わり
    if recipient != recipient_wallet_address_of_BDA:
        return {"status":"error", "details":"送金先のWavesウォレットアドレスが、BDA指定のものと異なります。" }

    # 受信アドレスが等しければ続きの情報を拾う
    # 送信主のアドレス
    sender = json_obj["sender"]
    # イーサートークン比率は比率は25:1
    eth_amount = amount / 25.0
    # 一応トランザクションID自体も控えておく
    transaction_id = json_obj["id"]
    # アタッチメントにイーサーウォレットのアドレスがあるはず
    attachment = json_obj["attachment"]

    # アタッチメントは、原文のままになる場合と、base58エンコードがかかる場合がある。
    try:
        # base58デコードした文字列を返す。失敗した場合原文文字列ままを返す。
        attachment = Base58DecodedWalletAddress.get_base58_decoded_wallet_address(attachment)
    except:
        attachment = ""
        # print("送金先イーサーアドレスエラー")

    # print(recipient)
    # print(sender)
    # print(amount)
    # print(eth_amount)
    # print(transaction_id)
    # print(attachment)

    # 基本情報をセッティング
    ret_dict = {
        "sender":sender,
        "amount":amount,
        "eth_amount":eth_amount,
        "transaction_id":transaction_id,
        "eth_address":attachment
    }

    # 送金者が、Attachmentに記載した情報が、イーサーアドレスとして不適切なことが明白であれば…
    # エラー情報を付加情報として記載しておく。
    # 送金自体はしてしまってるので特別な対処が必要かもしれない。
    if JudgeErrorWalletAddress.is_message_ether_pattern(attachment) != True:
        ret_dict["status"] = "error"
        ret_dict["details"] = "送金先のイーサーアドレスが不正です。"

    return ret_dict





# テスト
if __name__ == '__main__':
    test_json = r"""{
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

    # test_json = r'{ "status":"error", "details":"Transaction is not in blockchain" }'

    test_json2 = r"""{
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

    test_pyobj = json_to_python_obj(test_json)
    print(test_pyobj)