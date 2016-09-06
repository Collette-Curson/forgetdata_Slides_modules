import _csv

def GetCsvVal(file, name):
    global f
    f = _csv.reader(open(file, "r"))
    for row in f:
        if(row[0] == name):
            return row[1:]
        
    return "0"

def GetCsvVal2(name):
    global f
    f = _csv.reader(open("c:/temp/Spend.txt", "r"))
    for row in f:
        if(row[0] == name):
            return row[1]
        
    return "0"