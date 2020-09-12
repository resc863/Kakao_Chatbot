from bs4 import BeautifulSoup
import urllib, requests, re
import json
import datetime
from datetime import date

def cnt1():
    year=datetime.datetime.now().year
    month=datetime.datetime.now().month
    month=str(month)
    day=datetime.datetime.now().day 

    if len(str(month)) == 1 :
        month="0"+str(month)

    fanta=str(year)+str(month)+str(day)
    url="http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey=JGMlPMEcTuNV8sbu5JRfjhwjPXMdCv1OJ1qQefm0vVuKWGKtGHAcJEWtm63GOVyMQYAcI%2BoXUBe0nsJ4w3RiZw%3D%3D&pageNo=1&numOfRows=10&startCreateDt="+fanta+"&endCreateDt="+fanta #call back url
    test_url="http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey=JGMlPMEcTuNV8sbu5JRfjhwjPXMdCv1OJ1qQefm0vVuKWGKtGHAcJEWtm63GOVyMQYAcI%2BoXUBe0nsJ4w3RiZw%3D%3D&pageNo=1&numOfRows=10&startCreateDt=20200821&endCreateDt=20200821"

    print(url)

    cola=requests.get(url).text
    sida=BeautifulSoup(cola, "html.parser")
    items=sida.find("items")
    result = [0, 0, 0]

    for item in items :
        try:
            hapgae=item.find("gubun").string
        except:
            continue
        if hapgae == "합계" :
            try:
                incdec=item.find("incdec").string
                result[0]=incdec
            except:
                pass
        if hapgae == "부산" :
            try:
                incdec=item.find("incdec").string
                result[1]=incdec
            except:
                pass
        if hapgae == "합계" :
            try:
                deathcnt=item.find("deathcnt").string
                result[2]=deathcnt
            except:
                pass
    
    return result

def cnt2():
    year=datetime.datetime.now().year
    month=datetime.datetime.now().month
    month=str(month)
    day=datetime.datetime.now().day 

    if len(str(month)) == 1 :
        month="0"+str(month)

    fanta=str(year)+str(month)+str(day)
    if (day == 1):
        fanta1 = str(year)+str(month)+"28"
    else:
        fanta1 = str(year)+str(month)+str(int(day)-1)
    url="http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson?serviceKey=0XeO7nbthbiRoMUkYGGah20%2BfXizwc0A6BfjrkL6qhh2%2Fsl8j9PzfSLGKnqR%2F1v%2F%2B6AunxntpLfoB3Ryd3OInQ%3D%3D&pageNo=1&numOfRows=10&startCreateDt="+fanta1+"&endCreateDt="+fanta #call back url
    test_url="http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson?serviceKey=0XeO7nbthbiRoMUkYGGah20%2BfXizwc0A6BfjrkL6qhh2%2Fsl8j9PzfSLGKnqR%2F1v%2F%2B6AunxntpLfoB3Ryd3OInQ%3D%3D&pageNo=1&numOfRows=10&startCreateDt=20200821&endCreateDt=20200822"

    cola=requests.get(url).text
    sida=BeautifulSoup(cola, "html.parser")
    items=sida.find("items")
    result = [0, 0, 0]

    for item in items :
        try:
            decidecnt=item.find("decidecnt").string
            result[0]=decidecnt
        except:
            pass
        
        try:
            clearcnt=item.find("clearcnt").string
            result[1]=clearcnt
        except:
            pass

        try:
            deathcnt=item.find("deathcnt").string
            result[2]=deathcnt
        except:
            pass
        
    
    return result

if __name__ == "__main__":
    print(cnt1())
    print(cnt2())
