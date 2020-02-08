#-*-coding:utf-8-*-

from flask import Flask, request, jsonify
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib, requests, re
import json, sqlite3
import datetime
import time
import random
from datetime import date
import sys

ERROR_MESSAGE = '네트워크 접속에 문제가 발생하였습니다. 잠시 후 다시 시도해주세요.'


app = Flask(__name__)

def lineid(lineno):    
    lineurl = "http://61.43.246.153/openapi-data/service/busanBIMS2/busInfo?lineno="+lineno+"&serviceKey=0XeO7nbthbiRoMUkYGGah20%2BfXizwc0A6BfjrkL6qhh2%2Fsl8j9PzfSLGKnqR%2F1v%2F%2B6AunxntpLfoB3Ryd3OInQ%3D%3D"
    lineid2 = requests.get(lineurl).text
    lineid1 = BeautifulSoup(lineid2, "html.parser")
    lineid0 = lineid1.find('item')
    lineid = lineid0.lineid.string

    return lineid

def nextstop(no, lineno):
    lineid1 = lineid(lineno)
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

def bus():
    result = "양운고 앞 대림1차아파트 정보\n\n"
    bus1="186190402"
    bus2="186210101"
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
            result = "급식이 없습니다."
            return result
            
        elif len(d_diet) == 1:
            lunch = local_date + " 중식\n\n" + l_diet
            return lunch
        else:
            lunch = local_date + " 중식\n\n" + l_diet + "\n"
            dinner = local_date + " 석식\n\n" + d_diet
            meal = lunch + dinner
            return meal
        
def forecast() : #날씨 예보 파싱 함수

    y,m,d,h,mi = dayCal()
  
    key = 'ExhrDuBJZ28eMHPRIyFToDuqoT1Lx3ViPoI3uKVLS%2FyucnbaLbQISs4%2FSJWf0AzAV1gkbbtZK5GWvO9clF%2B1aQ%3D%3D'
    #발급받은 인증키
    url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData?serviceKey='+key+'&base_date='+y+m+d+'&base_time='+h+'00&nx=99&ny=75&numOfRows=90&pageNo=1&_type=json'
    #파싱할 json의 url
  
    rs = urlopen(url).read().decode('utf-8')
    #url주소를 읽어 내용을 'utf-8'형식으로 디코딩하여 문자열 반환
    json_data = json.loads(rs)
    #반환한 문자열을 json형식으로 읽음
    info = json_data.get("response").get("body").get("items").get("item")
   #필요한 정보부분만 따로 추출

    ft = str(info[0].get("fcstTime"))
    pop = ''
    pty = ''
    reh = ''
    sky = ''
    t3h = ''
    tmn = ''
    tmx = ''
    vec = ''
    wsd = ''
    apm = ''
    for i in range(len(info)) :
        cate = info[i].get("category");
        value = str(info[i].get("fcstValue"))
        if str(info[i].get("fcstTime")) == ft :
            if cate == 'POP' :
                pop = value
                #강수확률
            elif cate == 'PTY' :
                if value == '1' :
                    pty = ', 비'
                elif value == '2' :
                    pty = ', 비/눈'
                elif value == '3' :
                    pty = ', 눈/비'
                elif value == '4' :
                    pty = ', 눈'
            #강수형태
            elif cate == 'REH' :
                reh = value
            #습도
            elif cate == 'SKY' :
                if value == '1' :
                    sky = '맑음'
                elif value == '2' :
                    sky = '구름조금'
                elif value == '3' :
                    sky = '구름많음'
                elif value == '4' :
                    sky = '흐림'
            #하늘상태
            elif cate == 'T3H' :
                t3h = value
            #3시간 기온
            elif cate == 'WSD' :
                wsd = value
            #풍속
            if str(info[i].get("fcstTime")) == '1500' :
                if cate == 'TMX' :
                    tmx = value
            if str(info[i].get("fcstTime")) == '0600' :
                if cate == 'TMN' :
                    tmn = value
        
    if int(ft) < 1200 :
        apm = '오전 '
    elif int(ft) == 1200 :
        apm = '정오 '
    else :
        apm = '오후 '
        ft = str(int(ft)-1200)
        if int(ft) < 1000 :
            ft = '0'+ft

    p = apm+ft[:2]+':'+ft[2:]+' 예보\n\n최고 : '+tmx+'°C  최저 : '+tmn+'°C\n'+sky+pty+'\n'+t3h+'°C\n습도 : '+reh+'%\n강수확률 : '+pop+'%\n풍속 : '+wsd+'m/s'
 
    return p


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
            "dust": 'testing'
        }
    }
    return jsonify(result)

@app.route('/weather', methods=['POST'])
def weather():
    weather1 = forecast()
    print(weather1)
    result = {
        "version": "2.0",
        "data": {
            "weather": weather1
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
        result = {
            "version": "2.0",
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

@app.route('/schedule', methods=['POST'])
def schedule():
    today = datetime.date.today()

    try:
        officeCode="stu.pen.go.kr" ## 교육청 코드
        schulCode="C100000521" ## 학교 고유코드
        schulCrseCode="4" ## 학교 분류코드 (고등학교, 중학교, 초등학교)
        schulKndScCode="0" + "4" ## 학교 분류코드
        ay=today.year
        mm=today.month
    except:
        print("""!!ERROR.... 
                코드 인자 값이 맞지 않거나 값이 이상합니다.
                제대로 된 코드 값을 입력해주십쇼""")
        sys.exit(1)

    ##neis web requests
    URL="https://" + officeCode + "/sts_sci_sf01_001.do"
    ##params = {'schulCode': 'B100000593', 'schulCrseScCode': '4', 'schulKndScCode' : '04', 'ay' : str(year)} 
    params = {'schulCode': str(schulCode), 'schulCrseScCode': str(schulCrseCode), 'schulKndScCode' : str(schulKndScCode), 'ay' : str(ay), 'mm' : str(mm)}
    response = requests.get(URL, params=params).text
    data = response[response.find("<tbody>"):response.find("</tbody>")]

    ## re 정규표현식으로 불필요한 데이터를 자르거나 변환
    regex = re.compile(r'[\n\r\t]')
    data=regex.sub('',data)
    rex = re.compile(r'<div class="textL">(.*?)</div>', re.S|re.M)
    data=rex.findall(data)
    element = ""

    for dat in data:
        date=dat[dat.find("<em>"):dat.find("</em>")][4:]
        alert=dat[dat.find("<strong>"):dat.find("</strong>")][8:]
        if date == "":
            continue
        if alert == "":
            continue
    
        element = element+date+": "+alert+"\n"

    print(element)
    
    result = {
        "version": "2.0",
        "data": {
            "schedule": element
        }
    }
    
    return jsonify(result)

@app.route('/db', methods=['POST'])
def db():
    body = request.get_json()

    content = body['context']

    print(content)

    grade = body['action']['params']['학년'] #학년
    subject = body['action']['params']['과목'] #과목
    date = body['action']['params']['기한']['value']['date'] #마감기한
    content = body['context'][0]['params']['내용']['value'] #수행내용

    conn = sqlite3.connect("2019.db")
    cur = conn.cursor()
    
    print(grade)
    print(subject)
    print(date)

    data = "학년: "+grade+"\n"+"과목: "+subject+"\n"+"마감 기한: "+date+"\n"
    
    result = {
        "version": "2.0",
        "data": {
            "db": data
        }
    }
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

@app.route('/timetable_s', methods=['POST'])
def timetable_s():
    body = request.get_json()
    conn = sqlite3.connect("timetable.db")
    cur = conn.cursor()

    finds = body['action']['params']
    
    if finds==1:
        finds='one'
    elif finds==2:
        finds='two'
    elif finds==3:
        finds='three'
    elif finds==4:
        finds='four'
    elif finds==5:
        finds='five'
    elif finds==6:
        finds='six'
    elif finds==7:
        finds='seven'
    elif finds==8:
        finds='eight'
    elif finds==9:
        finds='nine'
    elif finds==10:
        finds='ten' 

    cur.execute('select * from %s'%finds)

    for row in cur:
        r = r + row + "\n"
    
    result = {
        "version": "2.0",
        "data": {
            "businfo": r
        }
    }
    return jsonify(result)

@app.route('/timetable_t', methods=['POST'])
def timetable_t():
    body = request.get_json()
    conn = sqlite3.connect("timetable.db")
    cur = conn.cursor()

    finds = body['action']['params']
    date = body['action']['params']
    time = body['action']['params']
    subjectf = body['action']['params']
    subjectc = body['action']['params']
    
    if finds==1:
        finds='one'
    elif finds==2:
        finds='two'
    elif finds==3:
        finds='three'
    elif finds==4:
        finds='four'
    elif finds==5:
        finds='five'
    elif finds==6:
        finds='six'
    elif finds==7:
        finds='seven'
    elif finds==8:
        finds='eight'
    elif finds==9:
        finds='nine'
    elif finds==10:
        finds='ten' 

    cur.execute('select * from %s'%finds)

    cur.execute("update %s set %s = '%s' where %s = '%s' and 교시 = '%s'" %(finds,date, subjectc, date, subjectf,time))
    try:
        conn.commit()
        ans = "정상적으로 처리되었습니다."
    except:
        ans = "오류가 발생했습니다."
    
    result = {
        "version": "2.0",
        "data": {
            "businfo": ans
        }
    }
    return jsonify(result)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, threaded=True)
