from bs4 import BeautifulSoup
from multiprocessing import Pool
import requests

def lineid(lineno):    
    lineurl = "http://61.43.246.153/openapi-data/service/busanBIMS2/busInfo?lineno="+lineno+"&serviceKey=0XeO7nbthbiRoMUkYGGah20%2BfXizwc0A6BfjrkL6qhh2%2Fsl8j9PzfSLGKnqR%2F1v%2F%2B6AunxntpLfoB3Ryd3OInQ%3D%3D"
    lineid2 = requests.get(lineurl).text
    lineid1 = BeautifulSoup(lineid2, "html.parser")
    lineid0 = lineid1.find('item')
    lineid = lineid0.lineid.string

    return lineid

def nextstop(l):
    no = l[0]
    lineno = l[1]

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

def getinfo(x):
    bus1="186190402"
    bus2="186210101"
    url1 = 'http://61.43.246.153/openapi-data/service/busanBIMS2/stopArr?serviceKey=ExhrDuBJZ28eMHPRIyFToDuqoT1Lx3ViPoI3uKVLS%2FyucnbaLbQISs4%2FSJWf0AzAV1gkbbtZK5GWvO9clF%2B1aQ%3D%3D&bstopid='+bus1
    url2 = 'http://61.43.246.153/openapi-data/service/busanBIMS2/stopArr?serviceKey=ExhrDuBJZ28eMHPRIyFToDuqoT1Lx3ViPoI3uKVLS%2FyucnbaLbQISs4%2FSJWf0AzAV1gkbbtZK5GWvO9clF%2B1aQ%3D%3D&bstopid='+bus2

    if x == '0':
        html = requests.get(url1).text
    else:
        html = requests.get(url2).text

    return html

def process(b):
    result = b.lineno.string + "번 버스" + "\n"
    lineno = b.lineno.string

    if b.arsno == None:
         no = "정보가 없습니다."
    else:
        no = b.arsno.string

    if no == "정보가 없습니다":
        nextstop1 = None
    else:
        l = [no, lineno]
        nextstop1 = nextstop(l)

    if nextstop1 == None:
        result = result + "다음역: 정보가 없습니다.\n"
    else:
        result = result + "다음역:" + nextstop1 + "\n"

    if b.min1==None:
        result = result + "현재 최근버스시간이 존재하지않습니다.\n\n"
    else:
        result = result + b.min1.string + "분 뒤 도착" + "\n\n"

    return result

def bus():
    result = "양운고 앞 대림1차아파트 정보\n\n"

    pool = Pool(processes=8)

    html = pool.map(getinfo, '0')[0]
    print("00000")
    html1 = pool.map(getinfo, '1')[0]
    print("22222")

    soup = BeautifulSoup(html, "html.parser")
    soup1 = BeautifulSoup(html1, "html.parser")
    item=soup.findAll('item')

    for b in item:
        r = process(b)
        result = result + r

    print("111111")

    result = result + "\n\n"

    item=soup1.findAll('item')

    for b in item:
        r = process(b)
        result = result + r

    return result
        
if __name__ == "__main__":
    print(bus())
