import argparse
import ftpmodule as ftpm
import fileValidation as fv
import datetime



def main(args):

    ftpm.downloadFiles(ftpm.getFTPConnetion(args.target), 
                       ".temp", "/", args.date)

    # Now check files
    valid = fv.runChecks("./.temp")
    print(valid)
    # Now store files


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