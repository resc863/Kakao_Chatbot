#-*-coding:utf-8-*-
# 주의:github 저장소에는 보안상의 이유로 토큰들을 누락함.

from flask import Flask, request, jsonify
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib, requests, re
import json, sqlite3
import datetime, time
import random, threading
from datetime import date
import sys
import count, bus, getdust, school_meal, school_schedule

ERROR_MESSAGE = '네트워크 접속에 문제가 발생하였습니다. 잠시 후 다시 시도해주세요.'

def auto(): # 수행평가 DB에서 기한이 만료된 수행평가를 삭제
    con = sqlite3.connect("2019.db") #DB 연결
    threading.Timer(3600*24, auto).start()

    cur = con.cursor()

    now = datetime.datetime.now() # 오늘 날짜 처리

    time = (str(now.year) + " " +  str(now.month) + " " + str(now.day))

    for cnt in range(1, 4):
        cur.execute("select count('month') from Suhang"+str(cnt))
        con.commit()
        rows=cur.fetchone()
        cur.execute("select month from Suhang"+str(cnt))
        con.commit()
        a=cur.fetchall()
        cur.execute("select day from Suhang"+str(cnt))
        con.commit()
        b=cur.fetchall()
        i=0
    
        for i in range(rows[0]):
            if a[i][0]==now.month:
                if b[i][0]==now.day:
                    print("Deleted")
                    cur.execute("delete from Suhang"+str(cnt)+" where day='%d'"%b[i][0])
                    con.commit()
                
    con.close()

app = Flask(__name__)

def maskinfo(location): # 공적마스크 조회 - 폐지됨
    location = urllib.parse.quote(location)
    url = "https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByAddr/json?address="+location

    html = urlopen(url).read().decode('utf-8')
    data = json.loads(html).get('stores')

    return data
        
def forecast() : #TODO: OpenWeatherMap API 키는 알아서 처리할것

    f = open("/home/kakao/weather_key.txt", "r")
    key = f.readline()
    url = "http://api.openweathermap.org/data/2.5/forecast?q=busan&cnt=10&units=metric&lang=kr&APPID="+key

    html = requests.get(url).text
    data = json.loads(html)

    name = data['city']['name']
    weather = data['list']
 
    return weather


@app.route('/keyboard')
def Keyboard():
    dataSend = {
    }
    return jsonify(dataSend)

@app.route('/tomorrow_meal', methods=['POST'])
def tomorrow_meal():
    request_body = request.get_json()  # request body 받음
    params = request_body['action']['params'] # action > params로 파라미터에 접근

    y = str(list(time.localtime(time.time()))[0])
    m = str(list(time.localtime(time.time()))[1])
    d = str(list(time.localtime(time.time()))[2])
    
    # 다음날을 구하기 위해 윤년, 2월, 30-31일을 고려할것
    
    if m == '12' and d == '31' :
        y = str(int(y)+1)
        m = '1'
        d = '1'
    elif d == '31' :
        if m == '1' or m == '3' or m == '5' or m == '7' or m == '8' or m == '10' :
            m = str(int(m)+1)
            d = '1'
    elif d == '30' :
        if m == '4' or m == '6' or m == '9' or m == '11' :
            m = str(int(m)+1)
            d = '1'
    elif d == '29' :
        if m == '2' and int(y)%4 == 0 :
            m = '3'
            d = '1'
    elif d == '28' :
        if m == '2' and int(y)%4 != 0 :
            m = '3'
            d = '1'
    else :
        d = str(int(d)+1)
        
    if int(m)<10 :
        m = '0'+m
    if int(d)<10 :
        d = '0'+d
    tomorrow = y+'.'+m+'.'+d

    tomorrow = str(tomorrow).replace(".", "")
    
    try : 
        whatday = time.localtime().tm_wday+1
        if whatday == 7 :
            whatday = 0
    except :
        result = {
            "version": "2.0",
            "data": {
                "tomorrow_meal": "급식이 없습니다."
            }
        }
        return jsonify(result)

    tomorrow_meal = school_meal.eat(tomorrow)
    print(tomorrow_meal)
    result = {
        "version": "2.0",
        "data": {
            "tomorrow_meal": tomorrow_meal
        }
    }
    return jsonify(result)
        
                                 
  
@app.route('/dust', methods=['POST'])
def dust():
    d = getdust.get_micro('좌동')
    print(d)
    result = {
        "version": "2.0",
        "data": {
            "dust": d
        }
    }
    return jsonify(result)

@app.route('/schedule', methods=['POST'])
def schedule():

    today = date.today()
    today = str(today).replace("-", "")

    data = school_schedule.school_schedule(today)
    
    result = {
        "version": "2.0",
        "data": {
            "schedule": data
        }
    }
    return jsonify(result)
  
@app.route('/test', methods=['POST'])
def test():
    print('test')
    result = {
        "version": "2.0",
        "data": {
            "test": 'testing'
        }
    }
    return jsonify(result)

@app.route('/weather', methods=['POST'])
def weather():
    weather1 = forecast()
    w = "부산 현재 날씨\n\n"

    for i in weather1:
        date = datetime.datetime.fromtimestamp(i['dt']).strftime('%Y-%m-%d %H:%M:%S')
        print("예보 시각: "+date)
        w = w + "예보 시각: "+date + "\n"
        temp = i['main']['temp']
        print("기온: "+str(temp))
        w = w + "기온: "+str(temp)+ " C" + "\n"
        feel = i['main']['feels_like']
        print("체감 기온: "+str(feel))
        humidity = i['main']['humidity']
        print("습도: "+str(humidity))
        w = w + "습도: "+str(humidity)+ " %" + "\n\n"
        cloud = i['weather'][0]['description']
        print("구름: "+cloud)
        print("="*20)

    result = {
        "version": "2.0",
        "data": {
            "weather": w
        }
    }
    return jsonify(result)
            
@app.route('/meal', methods=['POST'])
def meal():
    request_body = request.get_json()  # request body 받음
    params = request_body['action']['params'] # action > params로 파라미터에 접근
    
    today = date.today()
    today = str(today).replace("-", "")
    
    meal = school_meal.eat(today)
    print(meal)
    result = {
        "version": "2.0",
        "data": {
            "meal": meal
        }
    }
    
    return jsonify(result)

@app.route('/someday_meal', methods=['POST'])
def someday_meal():
    request_body = request.get_json()  # request body 받음
    params = request_body['action']['params'] # action > params로 파라미터에 접근

    print(params)

    j = params['날짜']
    j1 = json.loads(j)
    
    today = j1['value']

    today = str(today).replace("-", "")
    
    meal = school_meal.eat(today)
    print(meal)
    result = {
        "version": "2.0",
        "data": {
            "meal": meal
        }
    }
    
    return jsonify(result)
    
    return jsonify(result)

@app.route('/cnt', methods=['POST']) 
def cnt():
    data = count.cnt1()
    print(data)
    
    result = {
        "version": "2.0",
        "data": {
            "total": data[0],
            "cnt" : data[1],
            "death" : data[2]
        }
    }
    
    return jsonify(result)

@app.route('/total_cnt', methods=['POST']) 
def total_cnt():
    data = count.cnt2()
    print(data)
    
    result = {
        "version": "2.0",
        "data": {
            "total": data[0],
            "cnt" : data[1],
            "death" : data[2]
        }
    }
    
    return jsonify(result)

@app.route('/db', methods=['POST']) #수행평가 추가
def db():
    body = request.get_json()

    content = body['contexts'][0]['params']
    detail = body['action']['detailParams']
    print(content)
    print(detail)

    grade = content['학년']['resolvedValue'] #학년
    print(grade)
    
    subject = content['과목']['resolvedValue'] #과목
    print(subject)
    
    content1 = detail['내용']['value'] #수행내용
    print(content)

    pwd = detail['비밀번호']['origin'] #문자열
        
    date1 = body['action']['detailParams']['기한']['value'] #마감기한
    date = json.loads(date1)
    date = date['value']
    print(date)

    d = date.split("-")

    year = d[0]
    print(year)

    month = d[1]
    print(month)

    day = d[2]
    print(day)

    pwd = pwd + "\n"
    f = open("/home/kakao/kakao/password.txt", "r")
    pwd1 = f.readline()
    print(pwd)
    print(pwd1)

    if pwd == str(pwd1):
        print("일치")

    if pwd != pwd1:
        print("비밀번호가 맞지 않습니다")
        result = {
            "version": "2.0",
            "data": {
                "db": "비밀번호가 맞지 않습니다"
            }
        }
    
        return jsonify(result)
    
    conn = sqlite3.connect("2019.db")
    cur = conn.cursor()

    try:
        cur.execute("insert into Suhang"+grade+" values (?,?,?,?,?)", (year, month, day, content1, subject))
        conn.commit() 
        cur.execute("select * from Suhang"+grade+" where month="+ month +" and day="+ day)
        data = ""

        for row in cur:
            data = data+ ("과목 : " + str(row[4]) +'\n' +
                    "내용 : " + str(row[3]) + '\n' +
                    "날짜 : " + str(row[0]) + "년 " + str(row[1]) + "월 " + str(row[2]) +'일\n' +
                    "\n")
    except:
        data = "DB 오류!"
    
    
    print(data)
    
    result = {
        "version": "2.0",
        "data": {
            "db": data
        }
    }
    try:
        conn.close()
    except:
        print('Error')
    
    return jsonify(result)

@app.route('/search', methods=['POST']) #수행평가 검색
def search():
    body = request.get_json()

    content = body['contexts'][0]['params']

    print(content)

    grade = content['학년']['resolvedValue'] #학년
    print(grade)
    
    subject = content['과목']['resolvedValue'] #과목
    print(subject)
    

    conn = sqlite3.connect("2019.db")
    cur = conn.cursor()   
    
    cur.execute("select * from Suhang"+grade+" where subject='"+ subject+"'")
    data = ""

    for row in cur:
        data = data+ ("과목 : " + str(row[4]) +'\n' +
             "내용 : " + str(row[3]) + '\n' +
             "날짜 : " + str(row[0]) + "년 " + str(row[1]) + "월 " + str(row[2]) +'일\n' +
             "\n")

    print(data)
    
    result = {
        "version": "2.0",
        "data": {
            "search": data
        }
    }
    
    conn.close()
    
    return jsonify(result)
  
@app.route('/businfo', methods=['POST'])
def businfo():
    info = bus.bus()   
    
    result = {
        "version": "2.0",
        "data": {
            "businfo": info
        }
    }
    return jsonify(result)

@app.route('/timetable_s', methods=['POST']) #시간표 조회
def timetable_s():
    body = request.get_json()

    grade = body['action']['params']['학년']
    finds = body['action']['params']['반']

    if grade == "1":
        conn = sqlite3.connect("timetable1.db")
        cur = conn.cursor()
    
        cur.execute("select * from '"+finds+"'")
    elif grade == "2":
        conn = sqlite3.connect("timetable2.db")
        cur = conn.cursor()
    
        cur.execute("select * from '"+finds+"'")
    else:
        conn = sqlite3.connect("timetable3.db")
        cur = conn.cursor()
    
        cur.execute("select * from '"+finds+"'")
    

    a = '       월    화    수    목     금          \n'

    for row in cur:
        a = a + '   ' + str(row[0])+'   '+ str(row[1]) +'   '+str(row[2]) +'   '+str(row[3]) +'   '+str(row[4])+'   '+str(row[5] + "\n")
        a =  a + "\n"

    print(a)
    
    result = {
        "version": "2.0",
        "data": {
            "timetable": a
        }
    }
    return jsonify(result)

@app.route('/timetable_t', methods=['POST']) #시간표 수정
def timetable_t():
    body = request.get_json()
    conn = sqlite3.connect("timetable.db")
    cur = conn.cursor()

    finds = body['action']['params']['반']
    date = body['action']['params']['요일']
    time = body['action']['params']['교시']
    subjectc = body['action']['params']['과목2']
    
    cur.execute("update '%s' set %s = '%s' where %s != '%s' and 교시 = '%s'" %(finds, date, subjectc, date, subjectc,time))
    conn.commit()
    try:
        conn.commit()
        ans = "정상적으로 처리되었습니다."
    except:
        ans = "오류가 발생했습니다."
    
    result = {
        "version": "2.0",
        "data": {
            "timetable": ans
        }
    }
    return jsonify(result)

@app.route('/timetable_del', methods=['POST']) #시간표 삭제
def timetable_del():
    body = request.get_json()
    conn = sqlite3.connect("timetable.db")
    cur = conn.cursor()

    finds = body['action']['params']['반']
    date = body['action']['params']['요일']
    time = body['action']['params']['교시']
    subjectf = body['action']['params']['과목1']
    subjectc = body['action']['params']['과목2']
    
    cur.execute("update cla set %s = '%s' where %s != '%s' and 교시 = '%s'" %(date, subjectc, date, subjectc,time))
    try:
        conn.commit()
        ans = "정상적으로 처리되었습니다."
    except:
        ans = "오류가 발생했습니다."
    
    result = {
        "version": "2.0",
        "data": {
            "timetable": ans
        }
    }
    return jsonify(result)


if __name__ == '__main__':
    auto()
    app.run(host='0.0.0.0', port=5000, threaded=True)
