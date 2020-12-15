from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import urllib
import requests, re
import json
import datetime
from datetime import date

def school_schedule(date):
    date = date[0:6]
    url = "https://open.neis.go.kr/hub/SchoolSchedule?KEY=4ff568a5dd3d4b3e918eb4d1478096d7&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE=C10&SD_SCHUL_CODE=7150115&AA_YMD="+date
    result = ""

    html = requests.get(url).text
    js = json.loads(html)

    if ('SchoolSchedule' in js) == False:
        result = js['RESULT']['MESSAGE']
        
    else:
        for i in js['SchoolSchedule'][1]['row']:
            result = result + i['AA_YMD'][0:4] + "년 " + i['AA_YMD'][4:6] + "월 " + i['AA_YMD'][6:8] +"일\n"
            result = result + i['EVENT_NM'] + "\n\n"
    
    return result