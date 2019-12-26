from bs4 import BeautifulSoup
import requests

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
        result = result + b.lineno.string
    for b1 in item:
        if (b1.min1.string==None):
            result = result + "현재 최근버스시간이 존재하지않습니다."
        else:
            result = result + sex1.min1.string
        
bus()
