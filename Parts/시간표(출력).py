import sqlite3
 
conn = sqlite3.connect("timetable.db")
cur = conn.cursor()

def check():
    finds=int(input("반을 입력하세요:"))
    if finds==1:
        finds=1
    elif finds==2:
        finds=2
    elif finds==3:
        finds=3
    elif finds==4:
        finds=4
    elif finds==5:
        finds=5
    elif finds==6:
        finds=6
    elif finds==7:
        finds=7
    elif finds==8:
        finds=8
    elif finds==9:
        finds=9
    elif finds==10:
        finds=10
    return finds


def result(finds):
    cur.execute("select * from '%s'"%finds)

finds=check()    
result(finds)



def schedule():
    print('       월    화    수    목     금          ')
    a = ''
    for row in cur:
        a = a + '   ' + str(row[0])+'   '+ str(row[1]) +'   '+str(row[2]) +'   '+str(row[3]) +'   '+str(row[4])+'   '+str(row[5] + "\n")
        a =  a + "\n"
    return a
    
print(schedule())
