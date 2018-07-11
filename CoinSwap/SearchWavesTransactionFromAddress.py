import json
import WavesJsonToPythonObj
import GetWavesRecentTransactions
    
# 該当のWavesウォレットアドレスから直近100個のトランザクションを見つけ、指定のBDAのウォレットへと送金しているもののTransactionオブジェクトを得る。
# 個々のトランザクションの検証は、「WavesJsonToPythonObj.json_to_python_obj(...)」へと移譲している
def search_waves_transaction_from_address(str_waves_address):
    # wavesアドレスを元に、直近のトランザクション全部を引き出す
    list_json = GetWavesRecentTransactions.get_waves_recent_transactions_json(str_waves_address)
    # json文字列→pythonオブジェクトにする
    list_json_obj = json.loads(list_json)

    if "status" in list_json_obj and list_json_obj["status"] == "error":
        # print("error")
        return {"status":"error", "details":"対象のデータはトランザクションデータではありません。" }

    list_json_obj = list_json_obj[0]

    rtn_list = []

    # print(list_json_obj)
    for json_obj in list_json_obj:
        str_json = json.dumps(json_obj)
        try:
            ret = WavesJsonToPythonObj.json_to_python_obj(str_json)
            if "status" in ret and ret["status"] == "error":
                continue

            rtn_list.append(ret)
        except:
            pass

    return rtn_list





# テスト
if __name__ == '__main__':
    rtn_list = search_waves_transaction_from_address("3PM2LPgW8FjCsZDBivZ8gdVrYnJMM1vPQNx")

    print(rtn_list)

