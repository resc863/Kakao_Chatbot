from flask import Flask, request, jsonify
import json

ERROR_MESSAGE = 'Error 404'

app = Flask(__name__)

@app.route('/test1', methods=['POST'])
def test1():
    request_body = request.get_json()  # request body 받음
    params = request_body['action']['params'] # action > params로 파라미터에 접근
    
    data = params['test']

    dataSend = {
        "version": "2.0",
        "data": {
            "schedule": data
        }
    }

    return jsonify(dataSend)

@app.route('/test2', methods=['POST'])
def test2():
    request_body = request.get_json()  # request body 받음
    params = request_body['action']['params'] # action > params로 파라미터에 접근

    data = params['test']

    dataSend ={
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleImage": {
                        "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg",
                        "altText": "보물상자입니다"
                    }
                }
            ]
        }
    }
    
    return jsonify(dataSend)

@app.route('/test3')
def test3():
    request_body = request.get_json()  # request body 받음
    params = request_body['action']['params'] # action > params로 파라미터에 접근

    data = params['test']

    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
            {
                "basicCard": {
                    "title": "보물상자",
                    "description": "보물상자 안에는 뭐가 있을까",
                    "thumbnail": {
                        "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                    },
                    "profile": {
                        "imageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4BJ9LU4Ikr_EvZLmijfcjzQKMRCJ2bO3A8SVKNuQ78zu2KOqM",
                        "nickname": "보물상자"
                    },
                    "social": {
                        "like": 1238,
                        "comment": 8,
                        "share": 780
                    },
                    "buttons": [
                        {
                            "action": "message",
                            "label": "열어보기",
                            "messageText": "짜잔! 우리가 찾던 보물입니다"
                        },
                        {
                            "action":  "webLink",
                            "label": "구경하기",
                            "webLinkUrl": "https://e.kakao.com/t/hello-ryan"
                        }
                    ]
                }
            }
            ]
        }
    }
    
    return jsonify(dataSend)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)