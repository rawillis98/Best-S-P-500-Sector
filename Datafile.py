from numpy import genfromtxt
import numpy as np
import datetime

def utodt(unixDate):
    return datetime.datetime.fromtimestamp(int(unixDate)).strftime('%Y-%m-%d %H:%M:%S')

def ymdtodt(ymd):
    ymd = str(ymd).split('-')
    month = int(ymd[1])
    year = int(ymd[0])
    day = int(ymd[2])
            
    return datetime.date(year, month, day)

def dttoymd(dt):
    ymd = str(dt.year)
    if dt.month < 10:
        ymd += "0"
        ymd += str(dt.month)
    else:
        ymd += str(dt.month)
    if dt.day < 10:
        ymd += "0"
        ymd += str(dt.day)
    else:
        ymd += str(dt.day)
    return ymd




class Datafile:
    def __init__(self, file):
        self.fullpath = file
        self.name = file.split("\\")[8].split(".")[0]
        self.array = []
        with open(file) as f:
            firstRow = True
            for line in f:
                row = line[0:-1].split(',')
                if firstRow:
                    firstRow = False
                else:
                    row[0] = ymdtodt(row[0])
                    for col in range(1, len(row)):
                        row[col] = float(row[col])
                self.array.append(row)
        del self.array[0]
        self.array.reverse()

    def getToday(self, today):
        for row in range(len(self.array)):
            date = self.array[row][0]
            if today.year == date.year and today.month == date.month and today.day == date.day:
                return row
        return 'does not trade'
        
            
        
        
        

            





















    
