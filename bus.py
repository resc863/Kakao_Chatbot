from bs4 import BeautifulSoup
import requests

from bs4 import BeautifulSoup
import requests

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
        
print(bus())
