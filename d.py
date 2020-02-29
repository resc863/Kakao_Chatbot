import sqlite3
import datetime

con = sqlite3.connect("2019.db")


cur = con.cursor()

now = datetime.datetime.now()

time = (str(now.year) + " " +  str(now.month) + " " + str(now.day))
print(time)

cur.execute("select count('month') from Suhang")
con.commit()


rows=cur.fetchone()


cur.execute("select month from Suhang ")
con.commit()

a=cur.fetchall()


cur.execute("select day from Suhang")
con.commit()

b=cur.fetchall()

i=0
for i in range(rows[0]):
        if a[i][0]==now.month:
                if b[i][0]==now.day:
                        cur.execute("delete from Suhang where day='%d'"%b[i][0])
                        con.commit()
con.close()
