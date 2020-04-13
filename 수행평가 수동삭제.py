import sqlite3

con = sqlite3.connect("SU.db")

cur = con.cursor()

print("학년을 입력해주세요")

y=int(input())

print("삭제할 수행평가의 내용을 입력해주세요.")

content=input()

if y==1:
    z="Suhang1"
elif y==2:
    z="Suhang2"
elif y==3:
    z="Suhang3"

cur.execute("delete from "+z+" where name='%s'"%(content))

con.commit()
