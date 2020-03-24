import sqlite3

 

conn = sqlite3.connect("timetable.db")

 

cur = conn.cursor()

 



def check():
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
    return finds


def result(finds):
    cur.execute('select * from %s'%finds)

finds=check()    
result(finds)

for row in cur:

    print(row)
    

