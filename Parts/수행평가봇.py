import sqlite3

con = sqlite3.connect('2019.db')

cur=con.cursor()


print("몇월 수행평가를 출력하시겠습니까?")


x=input()
cur.execute("select * from Suhang where month="+ x)

cur.execute("insert into Suhang (year, month, day, name, subject) values ('2019', '12', '12', 'Hello', '미적분');")

def result ():
    a=""
    for row in cur:
        a = a+ ("과목 : " + str(row[4]) +'\n' +
             "내용 : " + str(row[3]) + '\n' +
             "날짜 : " + str(row[0]) + "년 " + str(row[1]) + "월 " + str(row[2]) +'일\n' +
             "\n")
    return a
        
print(result())

