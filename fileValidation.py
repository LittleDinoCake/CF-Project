import pandas as pd
import numpy as np

'''
TODO
- Empty files
    - Check for value present in row 0 col 0
- Incorrect filenames
    - Must be in format MED_DATA_YYYYMMDDHHMMSS.csv
    - ^ already part of download_ftp?
'''

def validEntries(filename):
    df = pd.read_csv(filename)
    df = df[["reading1", "reading2", "reading3", "reading4",
             "reading5", "reading6", "reading7", "reading8",
             "reading9","reading10"]]
    
    invalidEntries = df.iloc[np.where(df>9.999)]
    
    if (not invalidEntries.empty):
        returnCode = [filename, "Invalid data entered"]
        return returnCode
    else:
        return True

def emptyFile(filename):
    df = pd.read_csv(filename)
    if (df.empty):
        returnCode = [filename, "File is empty"]
        return returnCode
    else:
        return True
    


