import json
import Base58DecodedWalletAddress
import JudgeErrorWalletAddress

recipient_wallet_address_of_BDA = "3PFCT4q6K56zC8YGa8vBaXgvkfFvJnRdFF8"


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

def json_to_python_obj(str_json):

    json_obj = json.loads(str_json)

    if "status" in json_obj and json_obj["status"] == "error":
        # print("error")
        return {"status":"error", "details":"対象のデータはトランザクションデータではありません。" }
    else:
        recipient = json_obj["recipient"]
        if recipient == recipient_wallet_address_of_BDA:
            sender = json_obj["sender"]
            amount = json_obj["amount"] / 10.0
            eth_amount = amount / 25.0
            transaction_id = json_obj["id"]
            attachment = json_obj["attachment"]
            try:
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

            ret_dict = {
                "sender":sender,
                "amount":amount,
                "eth_amount":eth_amount,
                "transaction_id":transaction_id,
                "eth_address":attachment
            }

            if JudgeErrorWalletAddress.is_message_ether_pattern(attachment) != True:
                ret_dict["status"] = "error"
                ret_dict["details"] = "送金先のイーサーアドレスが不正です。"

            return ret_dict
        else:
            return {"status":"error", "details":"送金先のWavesウォレットアドレスが、BDA指定のものと異なります。" }


test_pyobj = json_to_python_obj(test_json)
print(test_pyobj)