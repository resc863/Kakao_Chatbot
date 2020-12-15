from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import urllib
import requests, re
import json
import datetime
from datetime import date

today = str(date.today())
today = today.replace("-", "")
print(today)

url = "https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=4ff568a5dd3d4b3e918eb4d1478096d7&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE=C10&SD_SCHUL_CODE=7150115&MLSV_YMD="+today
js = requests.get(url).text

data = json.loads(js)

print(len(data))

if ('mealServiceDietInfo' in data) == False:
    print(data['RESULT']['MESSAGE'])

else:
    for i in range (len(data['mealServiceDietInfo'][1]['row'])):
        if (data['mealServiceDietInfo'][1]['row'][i]['MMEAL_SC_CODE'] == '2') :
            lunch = data['mealServiceDietInfo'][1]['row'][i]['DDISH_NM']
            lunch = lunch.replace("<br/>", "\n")
            print("lunch:\n"+lunch)
    
        elif (data['mealServiceDietInfo'][1]['row'][i]['MMEAL_SC_CODE'] == '3'):
            dinner = data['mealServiceDietInfo'][1]['row'][i]['DDISH_NM']
            dinner = dinner.replace("<br/>", "\n")
            print("dinner:\n"+dinner)

