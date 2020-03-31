import sqlite3

con=sqlite3.connect("teacherx.db")

cur=con.cursor()

print("삭제시킬건가요 추가시킬건가요? (추가:1,수정:2)")

check=int(input())

print("몇반 시간표를 입력하실건가요?")

cla=int(input())


if check == 1:
    if cla == 1:
        n = 1
        while n <= 7:
            print("추가시킬 월요일 " + str(n) +"교시 과목이름을 입력하세요")
            m = input()
            print("추가시킬 화요일 " + str(n) +"교시 과목이름을 입력하세요")
            tu = input()
            print("추가시킬 수요일 " + str(n) +"교시 과목이름을 입력하세요")
            w = input()
            print("추가시킬 목요일 " + str(n) +"교시 과목이름을 입력하세요")
            tr = input()
            print("추가시킬 금요일 " + str(n) +"교시 과목이름을 입력하세요")
            f = input()
            con.commit()
            cur.execute("insert into class 1 values(?,?,?,?,?)",(m,tu,w,tr,f))
            con.commit()
            n += 1

if check == 2:
    print("무슨 요일을 수정하실건가요?")
    date = input()
    print("몇 교시를 수정하실건가요?")
    time = input()
    print("무슨 과목으로 수정하실건가요?")
    subjectc = input()
    
    cur.execute("update cla set %s = '%s' where %s != '%s' and 교시 = '%s'" %(date, subjectc, date, subjectc,time))
        
row=cur.fetchall()
con.commit()
print(row)
con.commit()
