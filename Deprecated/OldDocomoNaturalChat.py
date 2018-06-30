#2018/06/30で使えなくなる仕様

zatsudan_dict = {}
def get_zatsudan_taiwa_message(message):

    # 雑談対話APIを申請し、取得すること。
    BOTKEY = '************************************************************'
    #エンドポイントの設定
    endpoint = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY=REGISTER_KEY'
    url = endpoint.replace('REGISTER_KEY', BOTKEY)

    text = message.content

    content = ""
    id = str(message.author.id)
    if id in zatsudan_dict:
        content = zatsudan_dict[id]
    payload = {
        'utt' : text,
        'context': id,
        "nickname": "ディア",
        "nickname_y": "ディア",
        "sex": "女",
        "bloodtype": "B",
        "birthdateY": "1997",
        "birthdateM": "6",
        "birthdateD": "1",
        "age": "21",
        "constellations": "双子座",
        "place": "東京",
        "mode": "dialog"
    }
    headers = {'Content-type': 'application/json'}

    #送信
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    data = r.json()

    #jsonの解析
    response = data['utt']
    context = data['context']

    msg = '{0.author.mention} '.format(message) + response
    zatsudan_dict[id] = str(context)
    return msg
