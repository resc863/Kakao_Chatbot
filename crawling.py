import requests, json

url = "https://www.naver.com"

data1 = {
    "userRequest": {
        "timezone": "Asia/Seoul",
        "params": {},
        "block": {
            "id": "<블록 id>",
            "name": "<블록 이름>"
        },
        "utterance": "<사용자 발화>",
        "lang": "kr",
        "user": {
            "id": "<사용자 botUserKey>",
            "type": "botUserKey",
            "properties": {
                "plusfriendUserKey": "<카카오톡 채널 사용자 id>"
            }
        }
    },
    "contexts": [],
    "bot": {
        "id": "<봇 id>",
        "name": "<봇 이름>"
    },
    "action" : {
        "params" : {
            "test" : '5678'
        },
        "id": "<스킬 id>",
        "detailParams": {
            "test" : '5678'
        }
    }
}

req = requests.post('http://127.0.0.1:5000/test1', json=data1)

response = req.json()
print(response)