from flask import Flask, request, jsonify
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import urllib
import json

ERROR_MESSAGE = '네트워크 접속에 문제가 발생하였습니다. 잠시 후 다시 시도해주세요.'


app = Flask(__name__)

def get_diet(code, ymd, weekday):
    schMmealScCode = code #int 1조식2중식3석식
    schYmd = ymd #str 요청할 날짜 yyyy.mm.dd
    if weekday == 5 or weekday == 6: #토요일,일요일 버림
        element = " " #공백 반환
    else:
        num = weekday + 1 #int 요청할 날짜의 요일 0월1화2수3목4금5토6일 파싱한 데이터의 배열이 일요일부터 시작되므로 1을 더해줍니다.
        URL = (
                "http://stu.pen.go.kr/sts_sci_md01_001.do?"
                "schulCode=C100000521&schulCrseScCode=4"
                "&schulKndScCode=04"
                "&schMmealScCode=%d&schYmd=%s" % (schMmealScCode, schYmd)
            )
        #http://stu.pen.go.kr/ 관할 교육청 주소 확인해주세요.
        #schulCode= 학교고유코드
        #schulCrseScCode= 1유치원2초등학교3중학교4고등학교
        #schulKndScCode= 01유치원02초등학교03중학교04고등학교

        #기존 get_html 함수부분을 옮겨왔습니다.
        html = ""
        resp = requests.get(URL)
        if resp.status_code == 200 : #사이트가 정상적으로 응답할 경우
            html = resp.text
        soup = BeautifulSoup(html, 'html.parser')
        element_data = soup.find_all("tr")
        element_data = element_data[2].find_all('td')
        try:
            element = str(element_data[num])

            #filter
            element_filter = ['[', ']', '<td class="textC last">', '<td class="textC">', '</td>', '&amp;', '(h)', '.']
            for element_string in element_filter :
                element = element.replace(element_string, '')
            #줄 바꿈 처리
            element = element.replace('<br/>', '\n')
            #모든 공백 삭제
            element = re.sub(r"\d", "", element)

        #급식이 없을 경우
        except:
            element = " " # 공백 반환
    return element

def print_get_meal(local_date, local_weekday):
        l_diet = get_diet(2, local_date, local_weekday)
        d_diet = get_diet(3, local_date, local_weekday)

        if len(l_diet) == 1:
            result = {
                "version": "2.0",
                "data": {
                    "menu": "급식이 없습니다."
                }
            }
            
            return {
                'statusCode': 200,
                'body': json.dumps(result),
                'headers': {
                'Access-Control-Allow-Origin': '*',
                },
            }
        elif len(d_diet) == 1:
            lunch = local_date + " 중식\n" + l_diet
            return lunch
        else:
            lunch = local_date + " 중식\n" + l_diet
            dinner = local_date + " 석식\n" + d_diet
            meal = lunch + dinner
            return meal
            

def handler(event, context):
    request_body = json.loads(event['body']) # request body 받음
    params = request_body['action']['params'] # action > params로 파라미터에 접근
    date_obj = json.loads(params['date']) # 날짜 엔티티를 적용했을 경우 date가 객체로 넘어오기 때문에 파싱
    date = date_obj["date"] # date 객체에서 "yyyy-mm-dd" 형식의 date 데이터 추출
    date = date.replace("-", ".")

    s = date.replace('.', ', ') # 2017, 11, 21

        #한자리수 달인 경우를 해결하기위함
        if int(s[6:8]) < 10:
            s = s.replace(s[6:8], s[7:8])

        ss = "datetime.datetime(" + s + ").weekday()"
        try:
            whatday = eval(ss)
        except:
            return
    
    meal = print_get_meal(date, whatday)

    result = {
        "version": "2.0",
        "data": {
            "menu": meal
        }
    }

    return {
        'statusCode': 200,
        'body': json.dumps(result),
        'headers': {
        'Access-Control-Allow-Origin': '*',
        },
    }


@app.route('/meal', methods=['POST'])
def meal():
    req = request.get_json()
    menu = handler(req, )

    return jsonify(menu)



if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, threaded=True)