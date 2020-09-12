from bs4 import BeautifulSoup
import urllib, requests, re
from urllib.request import urlopen
import json
import datetime, time
from datetime import date

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

if __name__ == "__main__":
    print(get_micro('좌동'))