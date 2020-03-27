import sqlite3

con = sqlite3.connect('2019.db')

cur=con.cursor()


print("몇학년 정보를 원하십니까?") #학년 선택 버튼

grade = input("여기에 학년 입력")

x=input() # 2020 입력 함
cur.execute("select * from Suhang"+grade+" where year="+ x)#전체 정보 출력을 위해 년도로 선택 



def result ():   #정리 함수
    a=""
    for row in cur:
        a = a+ ("과목 : " + str(row[3]) +'\n' +
             "내용 : " + str(row[4]) + '\n' +
             "날짜 : " + str(row[0]) + "년 " + str(row[1]) + "월 " + str(row[2]) +'일\n' +
             "\n")
    return a
        
print(result())


