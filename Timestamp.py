from datetime import datetime
from time import mktime


### Fetching current time and storing them in variables ###
currentMinute = datetime.now().minute
currentHour = datetime.now().hour
currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year
previousMonth = 0


### Function finds what the date was for previous day and checks if its the beginning of a month ###
### add timestamp into daysInMonth dictionary ###
def previousDate(day, month, year):
    daysInMonth = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,

    }

    yesterday = {
        "month": month,
        "day": day,
        "year" : year
    }

    if (day - 1) == 0: # if that date is the first
        if month == 1: # if the month is january
            yesterday["month"] = 12
            yesterday["year"] -= 1
            yesterday["day"] = daysInMonth[12]
            return yesterday
        else: # if the month is not january
            yesterday["month"] -= 1
            yesterday["day"] = daysInMonth[yesterday["month"]]
            month -= 1
            return yesterday

    else:
        yesterday["day"] -= 1
        return yesterday



### fetches timestamp in EST for a given date ###
### Doesn't work when time is between 0am and 4am || After removing -4 from hour does it work? ###
def fetchTimestamp(year, month, day, hour,minute):
    dt = datetime(year, month, day, hour, minute)
    est = mktime(dt.timetuple())
    return est


### Grabs timestamps from 24 hours ago to current time ###
def twentyFourHours():
    timeStamps = {
        "time_from": 0,
        "time_to": 0,
    }
    yesterday = previousDate(currentDay, currentMonth, currentYear)
    timeStamps["time_from"] = fetchTimestamp(yesterday["year"], yesterday["month"], yesterday["day"], currentHour, currentMinute)
    timeStamps["time_to"] = fetchTimestamp(currentYear, currentMonth, currentDay, currentHour, currentMinute)
    return timeStamps

### Grabs timestamps from pasts hour ###
def pastThreeHours():
    timeStamps = {
        "time_from": 0,
        "time_to": 0,
    }
    timeStamps["time_from"] = fetchTimestamp(currentYear, currentMonth, currentDay, currentHour-3, currentMinute)
    timeStamps["time_to"] = fetchTimestamp(currentYear, currentMonth, currentDay, currentHour, currentMinute)
    return timeStamps



### Grabs timestamps from one year ago (within same hour) ###
def threeSixFive():
    timeStamps = {
        "time_from": 0,
        "time_to": 0,
    }
    timeStamps["time_from"] =fetchTimestamp(currentYear-1, currentMonth, currentDay, currentHour-1, currentMinute)
    timeStamps["time_to"] = fetchTimestamp(currentYear-1, currentMonth, currentDay, currentHour, currentMinute)
    return timeStamps
