import sqlite3

con = sqlite3.connect('2019.db')

cur = con.cursor()
cu = con.cursor()

print("문과입니까 이과 입니까?") #학년 선택 다음 나와야 됨


x=input() 
cur.execute("select * from Suhang where study = '%s'"%(x))
cu.execute("select * from Suhang where study = '공통'")


def result ():   #정리 함수
    a=""
    for row in cur:
        a = a+ ("과목 : " + str(row[3]) +'\n' +
                "내용 : " + str(row[4]) + '\n' +
                "날짜 : " + str(row[0]) + "년 " + str(row[1]) + "월 " + str(row[2]) +'일\n' +
                "\n")
        for row in cu:
            a = a+ ("과목 : " + str(row[3]) +'\n' +
                "내용 : " + str(row[4]) + '\n' +
                "날짜 : " + str(row[0]) + "년 " + str(row[1]) + "월 " + str(row[2]) +'일\n' +
                "\n")            
    return a
            
print(result())
