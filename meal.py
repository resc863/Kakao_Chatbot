from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import urllib
import requests, re
import json
import datetime
from datetime import date

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
            
            return "급식이 없습니다."
        
        elif len(d_diet) == 1:
            lunch = local_date + " 중식\n\n" + l_diet
            return lunch
        else:
            lunch = local_date + " 중식\n\n" + l_diet + "\n"
            dinner = local_date + " 석식\n\n" + d_diet
            meal = lunch + dinner
            return meal

#today = date.today()
today = "2019-11-11"
today1 = str(today).replace("-", ".")
s = today1.replace('.', ', ')
    #한자리수 달인 경우를 해결하기위함
if int(s[6:8]) < 10:
    s = s.replace(s[6:8], s[7:8])
ss = "datetime.datetime(" + s + ").weekday()"
try:
    whatday = eval(ss)
except:
    print("Error")
meal = print_get_meal(today, whatday)
print(meal)
