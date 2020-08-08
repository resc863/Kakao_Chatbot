import random, sqlite3

def timetable_s():
    body =  {
                'action' :  {
                    'params': {
                        '학년' : str(random.randrange(1, 4)),
                        '반' : str(random.randrange(1, 11))
                    }
                }
            }

    grade = body['action']['params']['학년']
    finds = body['action']['params']['반']

    if grade == "1":
        conn = sqlite3.connect("timetable1.db")
        cur = conn.cursor()
    
        cur.execute("select * from '"+finds+"'")
    elif grade == "2":
        conn = sqlite3.connect("timetable2.db")
        cur = conn.cursor()
    
        cur.execute("select * from '"+finds+"'")
    else:
        conn = sqlite3.connect("timetable3.db")
        cur = conn.cursor()
    
        cur.execute("select * from '"+finds+"'")
    

    a = '       월    화    수    목     금          \n'

    for row in cur:
        a = a + '   ' + str(row[0])+'   '+ str(row[1]) +'   '+str(row[2]) +'   '+str(row[3]) +'   '+str(row[4])+'   '+str(row[5] + "\n")
        a =  a + "\n"

    print(a)
    
    result = {
        "version": "2.0",
        "data": {
            "timetable": a
        }
    }
    return result

def test_timetable():
    t_db = timetable_s()
    assert t_db != None