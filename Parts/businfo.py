import requests, re
import parser
import urllib
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def stid(name,n):
    key = "0XeO7nbthbiRoMUkYGGah20%2BfXizwc0A6BfjrkL6qhh2%2Fsl8j9PzfSLGKnqR%2F1v%2F%2B6AunxntpLfoB3Ryd3OInQ%3D%3D"
    name = urllib.parse.quote(name)
    url = "http://61.43.246.153/openapi-data/service/busanBIMS2/busStop?serviceKey="+key+"&pageNo=1&numOfRows=10&bstopnm="+name
    try:
        doc = urllib.request.urlopen(url)
    except:
        print("Error!")
        return None
    xml1 = BeautifulSoup(doc,"html.parser")
    stopid2 = xml1.findAll('bstopid',string=True)

    try:
        if n == 1:
            stopid1 = str(stopid2[0])
            stopid = stopid1[9:18]
        elif n == 2:
            stopid1 = str(stopid2[1])
            stopid = stopid1[9:18]
    except:
        return None
    return stopid

def lineid(lineno):    
    lineurl = "http://61.43.246.153/openapi-data/service/busanBIMS2/busInfo?lineno="+lineno+"&serviceKey=0XeO7nbthbiRoMUkYGGah20%2BfXizwc0A6BfjrkL6qhh2%2Fsl8j9PzfSLGKnqR%2F1v%2F%2B6AunxntpLfoB3Ryd3OInQ%3D%3D"
    lineid2 = urllib.request.urlopen(lineurl)
    lineid1 = BeautifulSoup(lineid2, "html.parser")
    lineid0 = lineid1.find('item')
    lineid = lineid0.lineid.string

    return lineid

def nextstop(no, lineno):
    lineid1 = lineid(lineno)
    url = "http://61.43.246.153/openapi-data/service/busanBIMS2/busInfoRoute?lineid="+lineid1+"&serviceKey=0XeO7nbthbiRoMUkYGGah20%2BfXizwc0A6BfjrkL6qhh2%2Fsl8j9PzfSLGKnqR%2F1v%2F%2B6AunxntpLfoB3Ryd3OInQ%3D%3D"
    text = urllib.request.urlopen(url)
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
        
def info(station):
    id1 = stid(station, 1)
    id2 = stid(station, 2)

    if id1 == None or id2 == None:
        return "정보가 없습니다."
    key = "0XeO7nbthbiRoMUkYGGah20%2BfXizwc0A6BfjrkL6qhh2%2Fsl8j9PzfSLGKnqR%2F1v%2F%2B6AunxntpLfoB3Ryd3OInQ%3D%3D"
    url = "http://61.43.246.153/openapi-data/service/busanBIMS2/stopArr?serviceKey="+key+"&bstopid="+id1
    url1 = "http://61.43.246.153/openapi-data/service/busanBIMS2/stopArr?serviceKey="+key+"&bstopid="+id2
    
    try:
        inf1 = urllib.request.urlopen(url)
    except:
        print("Error!")
        return None
    info1 = BeautifulSoup(inf1, "html.parser")

    info="*"*20+"\n"
    
    for item in info1.findAll('item'):
        
        min1 = ""
        station1=""
        nextstop2 = ""
        no = ""

        if item.arsno == None:
            no = "정보가 없습니다."
        else:
            no = item.arsno.string

        lineno = item.lineno.string
        nextstop1 = nextstop(no, lineno)

        if item.min1 == None:
            min1 = "정보가 없습니다."
        else:
            min1 = item.min1.string

        if item.station1 == None:
            
            station1 = "정보가 없습니다."
        else:
            station1 = item.station1.string

        if nextstop1 == None:
            
            nextstop2 = "정보가 없습니다."

        else:
            nextstop2 = nextstop1
        
        info = info+"버스 번호:" +lineno +"\n"+"도착 시간:"+min1+"분"+"\n"+"남은 정류소 수:"+station1+"\n"+"다음 정류장: "+nextstop2+"\n"+"*"*20+"\n"

    try:
        inf2 = urllib.request.urlopen(url1)
    except:
        print("Error!")
        return None
    info2 = BeautifulSoup(inf2, "html.parser")

    info=info + "="*30+"\n"
    info=info + "*"*20+"\n"

    for item in info2.findAll('item'):
        
        min1 = ""
        station1=""
        nextstop2 = ""
        no = ""

        if item.arsno == None:
            no = "정보가 없습니다."
        else:
            no = item.arsno.string

        lineno = item.lineno.string
        nextstop1 = nextstop(no, lineno)

        if item.min1 == None:
            min1 = "정보가 없습니다."
        else:
            min1 = item.min1.string

        if item.station1 == None:
            
            station1 = "정보가 없습니다."
        else:
            station1 = item.station1.string

        if nextstop1 == None:
            
            nextstop2 = "정보가 없습니다."

        else:
            nextstop2 = nextstop1

        info = info+"버스 번호:" +lineno +"\n"+"도착 시간:"+min1+"\n"+"남은 정류소 수:"+station1+"\n"+"다음 정류장: "+nextstop2+"\n"+"*"*20+"\n"
        
    return info

print("=================================================")
print("=                                               =")
print("=        부산시 버스정보 검색 시스템            =")
print("=                                               =")
print("=================================================")

q = input("버스 정류장 입력: ")
print("\n검색중...\n")
a = info(q)
print(a)
