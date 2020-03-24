import sqlite3
import datetime

con = sqlite3.connect("Timecapsule.db")

cur = con.cursor()

now = datetime.datetime.now()

a = [31,28,31,30,31,30,31,30,31,30,31]
b = [31,29,31,30,31,30,31,30,31,30,31]


print("이름을 입력하세요 ")
name = str(input())

print("사연박스에 저장시킬 기간를 입력하세요(월)")
openmonth = int(input())

print("사연박스에 보관할 사연을 입력해주세요")
content = input()

x=0
y=now.year
i=0
if (y%4==0 and y%100!=0) or y&400==0:
    while i<openmonth:
        x=x+b[i]
        i=i+1
    now_after=now+datetime.timedelta(x)
    
    
else:
    while i<openmonth:
        x=x+a[i]
        i=i+1
    now_after=now+datetime.timedelta(x)
    

    
cur.execute("insert into save values(?,?,?,?)",(name,now,content,now_after))
con.commit()

print("저장되었습니다. 이용해주셔서 감사합니다.")
