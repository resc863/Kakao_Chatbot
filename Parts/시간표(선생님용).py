import sqlite3

conn=sqlite3.connect("timetable.db")

cur=conn.cursor()
          

finds=int(input("반을 입력하세요:"))

if finds==1:
    finds='one'
elif finds==2:
    finds='two'
elif finds==3:
    finds='three'
elif finds==4:
    finds='four'
elif finds==5:
    finds='five'
elif finds==6:
    finds='six'
elif finds==7:
    finds='seven'
elif finds==8:
    finds='eight'
elif finds==9:
    finds='nine'
elif finds==10:
    finds='ten'


print("무슨 요일을 수정하실건가요?")
date = input()
print("몇 교시를 수정하실건가요?")
time = input()
print("어떤 과목을 수정하실건가요?")
subjectf = input()
print("무슨 과목으로 수정하실건가요?")
subjectc = input()


cur.execute("update %s set %s = '%s' where %s = '%s' and 교시 = '%s'" %(finds,date, subjectc, date, subjectf,time))
conn.commit()

print("수정되었습니다.")

    
    
    
