import sqlite3

con = sqlite3.connect('2019.db')

cur=con.cursor()

cur.execute("insert into Suhang values ('2019', '12', '12', 'Hello', '미적분');")


con.commit()
con.close()
