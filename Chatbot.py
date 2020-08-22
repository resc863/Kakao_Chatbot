#-*-coding:utf-8-*-
# 주의:github 저장소에는 보안상의 이유로 토큰들을 누락함.

from flask import Flask, request, jsonify
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib, requests, re
import json, sqlite3
import datetime
import time
import random, threading
from datetime import date
import sys

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

def cnt1():
    year=datetime.datetime.now().year
    month=datetime.datetime.now().month
    month=str(month)
    day=datetime.datetime.now().day 

    if len(str(month)) == 1 :
        month="0"+str(month)

    fanta=str(year)+str(month)+str(day)
    url="http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey=JGMlPMEcTuNV8sbu5JRfjhwjPXMdCv1OJ1qQefm0vVuKWGKtGHAcJEWtm63GOVyMQYAcI%2BoXUBe0nsJ4w3RiZw%3D%3D&pageNo=1&numOfRows=10&startCreateDt="+fanta+"&endCreateDt="+fanta #call back url
    test_url="http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey=JGMlPMEcTuNV8sbu5JRfjhwjPXMdCv1OJ1qQefm0vVuKWGKtGHAcJEWtm63GOVyMQYAcI%2BoXUBe0nsJ4w3RiZw%3D%3D&pageNo=1&numOfRows=10&startCreateDt=20200821&endCreateDt=20200821"

    cola=requests.get(url).text
    sida=BeautifulSoup(cola, "html.parser")
    items=sida.find("items")
    result = [0, 0, 0]

    for item in items :
        try:
            hapgae=item.find("gubun").string
        except:
            continue
        if hapgae == "합계" :
            try:
                incdec=item.find("incdec").string
                result[0]=incdec
            except:
                pass
        if hapgae == "부산" :
            try:
                incdec=item.find("incdec").string
                result[1]=incdec
            except:
                pass
        if hapgae == "합계" :
            try:
                deathcnt=item.find("deathcnt").string
                result[2]=deathcnt
            except:
                pass
    
    return result

def cnt2():
    year=datetime.datetime.now().year
    month=datetime.datetime.now().month
    month=str(month)
    day=datetime.datetime.now().day 

    if len(str(month)) == 1 :
        month="0"+str(month)

    fanta=str(year)+str(month)+str(day)
    url="http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey=JGMlPMEcTuNV8sbu5JRfjhwjPXMdCv1OJ1qQefm0vVuKWGKtGHAcJEWtm63GOVyMQYAcI%2BoXUBe0nsJ4w3RiZw%3D%3D&pageNo=1&numOfRows=10&startCreateDt="+fanta+"&endCreateDt="+fanta #call back url
    test_url="http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey=JGMlPMEcTuNV8sbu5JRfjhwjPXMdCv1OJ1qQefm0vVuKWGKtGHAcJEWtm63GOVyMQYAcI%2BoXUBe0nsJ4w3RiZw%3D%3D&pageNo=1&numOfRows=10&startCreateDt=20200821&endCreateDt=20200821"

    cola=requests.get(url).text
    sida=BeautifulSoup(cola, "html.parser")
    items=sida.find("items")
    result = [0, 0, 0]

    for item in items :
        try:
            hapgae=item.find("gubun").string
        except:
            continue
        if hapgae == "합계" :
            try:
                defcnt=item.find("defcnt").string
                result[0]=defcnt
            except:
                pass
        if hapgae == "부산" :
            try:
                defcnt=item.find("defcnt").string
                result[1]=defcnt
            except:
                pass
        if hapgae == "합계" :
            try:
                deathcnt=item.find("deathcnt").string
                result[2]=deathcnt
            except:
                pass
    
    return result

def maskinfo(location): # 공적마스크 조회 - 폐지됨
    location = urllib.parse.quote(location)
    url = "https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByAddr/json?address="+location

    html = urlopen(url).read().decode('utf-8')
    data = json.loads(html).get('stores')

    return data

def lineid(lineno): # 버스노선 ID 조회   
    lineurl = "http://61.43.246.153/openapi-data/service/busanBIMS2/busInfo?lineno="+lineno+"&serviceKey=0XeO7nbthbiRoMUkYGGah20%2BfXizwc0A6BfjrkL6qhh2%2Fsl8j9PzfSLGKnqR%2F1v%2F%2B6AunxntpLfoB3Ryd3OInQ%3D%3D"
    lineid2 = requests.get(lineurl).text
    lineid1 = BeautifulSoup(lineid2, "html.parser")
    lineid0 = lineid1.find('item')
    lineid = lineid0.lineid.string

    return lineid

def nextstop(no, lineno): # 버스의 다음 정류장 조회
    lineid1 = lineid(lineno) # 현재 노선 ID
    url = "http://61.43.246.153/openapi-data/service/busanBIMS2/busInfoRoute?lineid="+lineid1+"&serviceKey=0XeO7nbthbiRoMUkYGGah20%2BfXizwc0A6BfjrkL6qhh2%2Fsl8j9PzfSLGKnqR%2F1v%2F%2B6AunxntpLfoB3Ryd3OInQ%3D%3D"
    text = requests.get(url).text
    soup = BeautifulSoup(text, "html.parser")
    nextidx = 0

    for item in soup.findAll('item'):
        bstop = ""
        
        if item.arsno == None:
            
            bstop = "정보가 없습니다."
        else:
            bstop = item.arsno.string
            
        curidx = int(item.bstopidx.string)
        
        if bstop == no:
            nextidx = curidx
            nextidx = nextidx + 1
            
        elif curidx == nextidx:
            nextstop = item.bstopnm.string
            return nextstop

def bus(): # TODO: 비동기 프로그래밍을 적용할것
    result = "양운고 앞 대림1차아파트 정보\n\n"
    bus1="186190402" # 상행
    bus2="186210101" # 하행
    url1 = 'http://61.43.246.153/openapi-data/service/busanBIMS2/stopArr?serviceKey=ExhrDuBJZ28eMHPRIyFToDuqoT1Lx3ViPoI3uKVLS%2FyucnbaLbQISs4%2FSJWf0AzAV1gkbbtZK5GWvO9clF%2B1aQ%3D%3D&bstopid='+bus1
    url2 = 'http://61.43.246.153/openapi-data/service/busanBIMS2/stopArr?serviceKey=ExhrDuBJZ28eMHPRIyFToDuqoT1Lx3ViPoI3uKVLS%2FyucnbaLbQISs4%2FSJWf0AzAV1gkbbtZK5GWvO9clF%2B1aQ%3D%3D&bstopid='+bus2
    
    html = requests.get(url1).text
    soup = BeautifulSoup(html, "html.parser")
    item=soup.findAll('item')

    for b in item:
        result = result + b.lineno.string + "번 버스" + "\n"
        lineno = b.lineno.string

        if b.arsno == None:
            no = "정보가 없습니다."
        else:
            no = b.arsno.string

        if no == "정보가 없습니다":
            nextstop1 = None
        else:
            nextstop1 = nextstop(no, lineno)

        if nextstop1 == None:
            result = result + "다음역: 정보가 없습니다.\n"
        else:
            result = result + "다음역:" + nextstop1 + "\n"

        if b.min1==None:
            result = result + "현재 최근버스시간이 존재하지않습니다.\n\n"
        else:
            result = result + b.min1.string + "분 뒤 도착" + "\n\n"

    result = result + "\n\n"

    html = requests.get(url2).text
    soup = BeautifulSoup(html, "html.parser")
    item=soup.findAll('item')

    for b in item:
        result = result + b.lineno.string + "번 버스" + "\n"
        lineno = b.lineno.string

        if b.arsno == None:
            no = "정보가 없습니다."
        else:
            no = b.arsno.string

        if no == "정보가 없습니다":
            nextstop1 = None
        else:
            nextstop1 = nextstop(no, lineno)

        if nextstop1 == None:
            result = result + "다음역: 정보가 없습니다.\n"
        else:
            result = result + "다음역:" + nextstop1 + "\n"

        if b.min1==None:
            result = result + "현재 최근버스시간이 존재하지않습니다.\n\n"
        else:
            result = result + b.min1.string + "분 뒤 도착" + "\n\n"
        

    return result

def dating(self) :
  self = str(self)
  y = self[:4]
  m = self[4:6]
  d = self[6:8]
  if len(self) == 10 :
    h = self[8:10]
    return y+"년 "+m+"월 "+d+"일 "+h+"시"
  return y+"년 "+m+"월 "+d+"일"

def get_micro(ar) : #대기질 정보 파싱 함수
  area = {'광복동':'221112', '초량동':'221131', '태종대':'221141', '전포동':'221152', '온천동':'221162','명장동':'221163', '대연동':'221172', '학장동':'221181', '덕천동':'221182', '청룡동':'221191', '좌동':'221192', '장림동':'221202', '대저동':'221211', '녹산동':'221212', '연산동':'221221', '기장음':'221231', '용수리':'221233', '수정동':'221241', '부곡동':'221251', '광안동':'221271', '대신동':'221281'}
  #측정기 지역 및 지역 번호
  key = 'ExhrDuBJZ28eMHPRIyFToDuqoT1Lx3ViPoI3uKVLS%2FyucnbaLbQISs4%2FSJWf0AzAV1gkbbtZK5GWvO9clF%2B1aQ%3D%3D'
  #발급받은 공공 인증키
  url = 'http://apis.data.go.kr/6260000/AirQualityInfoService/getAirQualityInfoClassifiedByStation?serviceKey='+key+'&numOfRows=1&resultType=json&areaIndex='
  #파싱할 json의 url

  ar = str(ar)
  #지역 입력
  p=""
  if ar == "주소" :
    for i in area.keys() :
      p = p + i+" : '"+url+area[i]+"'\n"
    return p
  #명령이 '주소'라면 모든 지역의 json주소를 출력
  elif ar not in area.keys() : 
    return "검색불가"
  #존재하지 않은 지역이라면 "검색불가" 반환 후 함수 탈출
  else :
    rs = urlopen(url+area[ar]).read().decode('utf-8')
    #url주소를 읽어 내용을 'utf-8'형식으로 디코딩하여 문자열 반환ㅌ
    json_data = json.loads(rs)
    #반환한 문자열을 json형식으로 읽음
    info = json_data.get("getAirQualityInfoClassifiedByStation").get("item")[0]
    #필요한 정보부분만 따로 추출

    controlnumber = dating(info.get("controlnumber"))
    #측정시간
    pm10 = info.get("pm10")
    #pm10
    if info.get("pm10Cai") == '1' :
      pm10Cai = "좋음" 
    elif info.get("pm10Cai") == '2' : 
      pm10Cai = "보통" 
    elif info.get("pm10Cai") == '3' :
      pm10Cai = "나쁨"
    elif info.get("pm10Cai") == '4' :
      pm10Cai = "매우나쁨"
    else :
      pm10Cai = "측정불가"
    #pm10 지수
    pm25 = info.get("pm25")
    #pm25
    if info.get("pm25Cai") == '1' :
      pm25Cai = "좋음" 
    elif info.get("pm25Cai") == '2' : 
      pm25Cai = "보통" 
    elif info.get("pm25Cai") == '3' :
      pm25Cai = "나쁨"
    elif info.get("pm25Cai") == '4' :
      pm25Cai = "매우나쁨"
    else :
      pm25Cai = "측정불가"
    #pm2.5 지수

    return "측정 정보\n\n"+controlnumber+"에 측정됨\n\npm10 (미세먼지) : "+pm10+"μm/m³ ("+pm10Cai+")\npm2.5 (초미세먼지) : "+pm25+"μm/m³ ("+pm25Cai+")"

def dayCal() :
  y=str(list(time.localtime(time.time()))[0])
  m=str(list(time.localtime(time.time()))[1])
  d=str(list(time.localtime(time.time()))[2])
  h=str(list(time.localtime(time.time()))[3])
  mi=str(list(time.localtime(time.time()))[4])
  
  
  if h != '2' and h != '5' and h!= '8' and h!= '11' and h != '14' and h != '17' and h != '20' and h != '23' :
    a = int(h)%3
    h=str(int(h)-a-1)
  else :
    if int(mi)<15 :
      h = str(int(h)-3)

  if int(h) < 0 :
    h = '23'
    if d == '1' :
        if m == '1' :
            y = str(int(y)-1)
            m = '12'
            d = '31'
        elif m == '5' or m == '7' or m == '8' or m == '10' or m == '12' :
            m = str(int(m)-1)
            d = '30'
        elif m == '2' or m == '4' or m == '6' or m == '9' or m == '11' :
            m = str(int(m)-1)
            d = '31'
        elif m == '3' and int(y)%4 == 0 :
            m = '2'
            d = '29'
        elif m == '3' and int(y)%4 != 0 :
            m = '2'
            d = '28'
    else :
        d = str(int(d)-1)

  if int(h)<10 :
    h = '0'+h
  if int(m)<10 :
    m = '0'+m
  if int(d)<10 :
    d = '0'+d
  if int(mi)<10 :
    mi = '0'+mi

  return y,m,d,h,mi



def get_diet(code, ymd, weekday):
    schMmealScCode = code #1 조식 2 중식 3 석식
    schYmd = ymd #요청할 날짜
    if weekday == 5 or weekday == 6: #토요일,일요일
        element = " " #공백 반환
    else:
        num = weekday + 1 
        URL = (
                "http://stu.pen.go.kr/sts_sci_md01_001.do?" # 작동이 안될시 수정할것
                "schulCode=C100000521&schulCrseScCode=4"
                "&schulKndScCode=04"
                "&schMmealScCode=%d&schYmd=%s" % (schMmealScCode, schYmd)
            )
        html = ""
        resp = requests.get(URL)
        if resp.status_code == 200 :
            html = resp.text
        soup = BeautifulSoup(html, 'html.parser')
        element_data = soup.find_all("tr")
        element_data = element_data[2].find_all('td')
        try:
            element = str(element_data[num])

            
            element_filter = ['[', ']', '<td class="textC last">', '<td class="textC">', '</td>', '&amp;', '(h)', '.']
            for element_string in element_filter :
                element = element.replace(element_string, '')
            #줄 바꿈 처리
            element = element.replace('<br/>', '\n')
          
            element = re.sub(r"\d", "", element)

        #급식이 없을 경우
        except:
            element = " " 
    return element

def print_get_meal(local_date, local_weekday):
        l_diet = get_diet(2, local_date, local_weekday) # 점심
        d_diet = get_diet(3, local_date, local_weekday) # 저녁

        if len(l_diet) == 1:
            result = "급식이 없습니다."
            return result
            
        elif len(d_diet) == 1: # 중식만 있을경우
            lunch = local_date + " 중식\n\n" + l_diet
            return lunch
        else:
            lunch = local_date + " 중식\n\n" + l_diet + "\n"
            dinner = local_date + " 석식\n\n" + d_diet
            meal = lunch + dinner
            return meal
        
def forecast() : #TODO: OpenWeatherMap API 키는 알아서 처리할것

    f = open("/root/weather_key.txt", "r")
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

    tomorrow_meal = print_get_meal(tomorrow, whatday)
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
    d = get_micro('좌동')
    print(d)
    result = {
        "version": "2.0",
        "data": {
            "dust": d
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
    today = str(today).replace("-", ".")
    
    try : 
      whatday = datetime.datetime.now().weekday()
    except :
        result = {   # 전송 양식
            "version": "2.0", # 스킬 버전
            "data": {
                "meal": "급식이 없습니다."
            }
        }
        return jsonify(result)
    
    print(str(today)+"\n"+str(whatday))
    meal = print_get_meal(today, whatday)
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
    d = today.split('-')
    year = d[0]
    month = d[1]
    day = d[2]

    today = str(today).replace("-", ".")
    
    try : 
      whatday = datetime.datetime(int(year), int(month), int(day)).weekday()
    except :
        result = {   # 전송 양식
            "version": "2.0", # 스킬 버전
            "data": {
                "meal": "급식이 없습니다."
            }
        }
        return jsonify(result)
    
    print(str(today)+"\n"+str(whatday))
    meal = print_get_meal(today, whatday)
    print(meal)
    result = {
        "version": "2.0",
        "data": {
            "meal": meal
        }
    }
    
    return jsonify(result)

@app.route('/schedule', methods=['POST']) # NEIS 크롤링 문제 발생 TODO: DB를 구축할것
def schedule():
    
    
    result = {
        "version": "2.0",
        "data": {
            "schedule": "현재 기능이 제공되지 않습니다"
        }
    }
    
    return jsonify(result)

@app.route('/cnt', methods=['POST']) 
def cnt():
    data = cnt1()
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
    data = cnt2()
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
    f = open("/root/password.txt", "r")
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
    info = bus()   
    
    result = {
        "version": "2.0",
        "data": {
            "businfo": info
        }
    }
    return jsonify(result)

@app.route('/mask', methods=['POST']) # 폐지
def mask():
    info = maskinfo("부산광역시 해운대구 좌동")  

    data = ""
    stat = ""
    
    for i in range(len(info)):
        try:
            if info[i]['remain_stat'] == 'empty':
                stat = "재고 없음"
            elif (info[i]['remain_stat'] == 'some') or (info[i]['remain_stat'] == 'plenty') or (info[i]['remain_stat'] == 'few'):
                stat = "재고 있음"

            else:
                stat = "알 수 없음"
        except:
            stat = "알 수 없음"
            
        data = data + info[i]['name'] + " : " +stat + "\n" +"주소: "+info[i]['addr']+"\n\n"

    print(data)

    result = {
        "version": "2.0",
        "data": {
            "mask": "공적마스크 제도는 폐지되었습니다"
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
