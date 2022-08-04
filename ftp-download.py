import re
import os
from ftplib import FTP
import argparse
from datetime import datetime

def downloadFiles(ftp, local_temp_dir, remote_dir, limit_date=None):
    if not os.path.isdir(local_temp_dir):
        print("Creating temporary directory")
        os.mkdir(local_temp_dir)



    # Grabs all files in specified dir
    file_list = ftp.nlst(remote_dir)

    # Compiles a regex that matches the file name format.
    # YYYYMMDDHHMMSS is exactly 14 digits of 1-9 with MED_DATA_ before and .csv after
    # It's case-insensitive so MeD_DaTA_ and .Csv would be allowed

    # TODO: More specific to time and date digit limits
    pattern = re.compile("(?i)(MED_DATA_)([0-9]{14})\.(csv)")

    totalDown = 0

    for file_name in file_list:

        # Matches the file name against the regex pattern
        if (pattern.match(file_name)):
            print(f"Found valid medical data: {file_name}")

            formatted_file_name, dt = getFileNameDate(file_name)

            # Check file date against provided date if given and skip any that don't match
            if limit_date != None:
                if dt.date() != limit_date.date():
                    print(f"Skipping {file_name} as not for today")
                    continue


            # Opens a new file in write-binary mode, downloads the CSV files in binary and writes directly into the open file
            # Then closes file after finished resulting in the contents being transfered over
            with open(os.path.join(local_temp_dir, formatted_file_name), "wb") as f:
                ftp.retrbinary(f"RETR {file_name}", f.write)
                totalDown += 1

            print(f"Downloaded {file_name} with datetime: {dt}")

    print(f"Downloaded {totalDown} MED_DATA files")


def getFileNameDate(file):
    # Get properly formatted name first (force to MED_DATA_YYYYMMDDHHMMSS.csv)
    split_name = file.split(".")
    formatted_file_name = split_name[0].upper() + "." + split_name[1].lower()

    # The first part of split name is MED_DATA_TIMEHERE so if we split again on _ and get the last item we get the tiem string
    datetimeString = split_name[0].split('_')[2]

    dt = datetime.strptime(datetimeString, '%Y%m%d%H%M%S')

    return (formatted_file_name, dt)

def getFTPConnetion(target):
    ftp = None
    try:
        print("Connecting to FTP")
        ftp = FTP(target)
        ftp.login()
        print("Connected to FTP")

    except Exception as e:
        print("Failed to connect to the FTP server. Aborting!\n")
        exit()

    return ftp

def main(args):

    downloadFiles(getFTPConnetion(args.target), ".temp", "/", args.date)

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Invalid date: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Program Parser")
    parser.add_argument('target', help="The target FTP server address")
    parser.add_argument('-d', '--date', type=valid_date, help="Download all med-data for the given date")
    args = parser.parse_args()
    main(args)
