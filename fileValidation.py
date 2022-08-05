import pandas as pd
import numpy as np
import time

def validEntries(filename):
    df = pd.read_csv(filename)
    df = df[["reading1", "reading2", "reading3", "reading4",
             "reading5", "reading6", "reading7", "reading8",
             "reading9","reading10"]]
    
    invalidEntries = df.iloc[np.where(df>9.999)]
    
    if (not invalidEntries.empty):
        returnCode = [filename, time.ctime(), "Invalid data entered"]
        return returnCode
    else:
        return True

def emptyFile(filename):
    df = pd.read_csv(filename)
    if (df.empty):
        returnCode = [filename, time.ctime(), "File is empty"]
        return returnCode
    else:
        return True
    

def checkUniqueBatch(filename):
    string = openFile(filename)
    textList = string.split("\n")
    batchList = []
    for i in range (1,len(textList)-1):
        line = textList[i].split(",")
        batchList.append(line[0])
    batchList.sort()
    uniqueBatchList = list(set(batchList))
    uniqueBatchList.sort()
    print(batchList)
    print(uniqueBatchList)
    if (batchList == uniqueBatchList):
        return True
    else:
        return [filename, time.ctime(), "Repeated Batch ID"]

def checkHeaders(filename):
    string = openFile(filename)
    textList = string.split("\n")
    if (textList[0] == "\"batch_id\",\"timestamp\",\"reading1\",\"reading2\",\"reading3\",\"reading4\",\"reading5\",\"reading6\",\"reading7\",\"reading8\",\"reading9\",\"reading10\""):
        return True
    else:
        return [filename, time.ctime(), "Incorrect Headers"]

def checkColumns(filename):
    string = openFile(filename)
    textList = string.split("\n")
    for i in range (1,len(textList)-1):
        line = textList[i].split(",")
        if len(line) != 12:
            return [filename, time.ctime(), "Incorrect Row Length"]
        else:
            return True

def openFile(filename):
    f = open("rawData.csv")
    return(f.read())

def addLog(logArray):
    filename = logArray[0]
    timestamp = logArray[1]
    errorType = logArray[2]
    f = open ("log.txt",'a')
    f.append(filename,timestamp,errorType)
    f.close()

