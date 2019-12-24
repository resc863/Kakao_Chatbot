from bs4 import BeautifulSoup
import requests

def sexy():
    sexy1="186190402"
    sexy2="186210101"
    url1 = 'http://61.43.246.153/openapi-data/service/busanBIMS2/stopArr?serviceKey=ExhrDuBJZ28eMHPRIyFToDuqoT1Lx3ViPoI3uKVLS%2FyucnbaLbQISs4%2FSJWf0AzAV1gkbbtZK5GWvO9clF%2B1aQ%3D%3D&bstopid='+sexy1
    url2 = 'http://61.43.246.153/openapi-data/service/busanBIMS2/stopArr?serviceKey=ExhrDuBJZ28eMHPRIyFToDuqoT1Lx3ViPoI3uKVLS%2FyucnbaLbQISs4%2FSJWf0AzAV1gkbbtZK5GWvO9clF%2B1aQ%3D%3D&bstopid='+sexy2
    
    html = requests.get(url1).text
    soup = BeautifulSoup(html, "html.parser")
    item=soup.findAll('item')
    for sex in item:
        print(sex.lineno.string)
    for sex1 in item:
        if (sex1.min1.string==None):
            print("현재 최근버스시간이 존재하지않습니다.")
        else:
            print(sex1.min1.string)
        
sexy()
