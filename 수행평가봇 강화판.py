import sqlite3

con = sqlite3.connect('SU.db')

cur=con.cursor()


print("몇월 수행평가를 출력하시겠습니까?")


x=input()

print("몇학년입니까?")

y=int(input())

if y==1:
    z="Suhang1"
elif y==2:
    z="Suhang2"
elif y==3:
    z="Suhang3"



cur.execute("select * from "+z+" where month="+ x)


def result ():
    a=""
    for row in cur:
        a = a+ ("과목 : " + str(row[4]) +'\n' +
             "내용 : " + str(row[3]) + '\n' +
             "날짜 : " + str(row[0]) + "년 " + str(row[1]) + "월 " + str(row[2]) +'일\n' +
             "\n")
    return a
        
print(result())
