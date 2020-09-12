import school_meal
import datetime
from datetime import date


if __name__ == '__main__':
    today = date.today()
    today1 = str(today).replace("-", ".")
    s = today1.replace('.', ', ')
    #한자리수 달인 경우를 해결하기위함
    if int(s[6:8]) < 10:
        s = s.replace(s[6:8], s[7:8])
    ss = "datetime.datetime(" + s + ").weekday()"
    try:
        whatday = eval(ss)
    except:
        print("Error")
    meal = school_meal.print_get_meal(today, whatday)
    print(meal)