import sqlite3

conn = sqlite3.connect("timetable.db")
cur = conn.cursor()

def check():
    finds=str(input("반을 입력하세요:"))
    return finds


def result(finds):
    cur.execute("select * from '"+finds+"'")

finds=check()    
result(finds)
r = ""

for row in cur:

    r = r + str(row) + "\n"

print(r)
    

