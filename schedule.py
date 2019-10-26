# -*- coding: utf-8 -*-
from datetime import *

try:
    from bs4 import BeautifulSoup
    import requests, re
except ImportError:
    try:
        print("Auto Installing requests, bs4")
        import pip
        pip.main(['install','bs4'])
        pip.main(['install','requests'])

        import requests, re
        from bs4 import BeautifulSoup
    except:
        raise ImportError("Error on importing modules")

print(datetime.today().year)
print(datetime.today().month)

def schedule():
    year=str(datetime.today().year)
    month=str(datetime.today().month)
    
    url = "https://stu.pen.go.kr/sts_sci_sf01_001.do?schulcode=C100000521&schulCrseScCode=4&schulKndScCode=04&ay="+year+"&mm="+month+"&"
    r = requests.get(url)
    print(r.text)
    soup = BeautifulSoup(r.text, "html.parser")

schedule()
