import requests, re, json, sys, datetime
from datetime import date

today = date.today()

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
