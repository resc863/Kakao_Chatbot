import sqlite3

con = sqlite3.connect('2019.db')

cur=con.cursor()


print("몇월 수행평가를 출력하시겠습니까?")


x=input()
cur.execute("select * from Suhang where month="+ x)


def result ():
    for row in cur:
        a = ("과목 : " + str(row[4]) +'\n' +
             "이름 : " + str(row[3]) + '\n' +
             "날짜 : " + str(row[0]) + " - " + str(row[1]) + " - " + str(row[2]) +'\n' +
             " ")
    return a
        
result()
