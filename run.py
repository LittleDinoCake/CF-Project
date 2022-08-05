import argparse
from datetime import datetime
import ftpmodule as ftpm
import fileValidation as fv

import os
import shutil


def storeFiles(files, temp_dir):
    # Grab date from file name and save hierachly

    for file in files:
        _, date = ftpm.getFileNameDate(file)
        dirs = datetime.strftime(date, "%Y/%m/%d")

        dir = "medical_data/" + dirs

        # Create the directory tree if it doesn't exist
        if not os.path.isdir(dir):
            os.makedirs(dir)

        # Copies files from temp to permanent
        shutil.copy(temp_dir + "/" + file, "./" + dir + "/" + file)

    # Deletes the temporary directory to cleanp
    shutil.rmtree(temp_dir)

    print(f"\n\n{len(files)} files have been saved into 'medical_data'!\nGoodbye!")





def main(args):

    # Download files
    ftpm.downloadFiles(ftpm.getFTPConnetion(args.target), 
                       ".temp", "/", args.date)

    # Now check files
    validFiles = fv.runChecks("./.temp")

    # Now store files
    storeFiles(validFiles, "./.temp")


# Used in argparse
def valid_date_format(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Invalid date: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)


# Start point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Program Parser")
    parser.add_argument('target', help="The target FTP server address")
    parser.add_argument('-d', '--date', type=valid_date_format, 
                        help="Download all med-data for the given date")
    args = parser.parse_args()
    main(args)