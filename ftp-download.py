import re
import os
from ftplib import FTP

print("Connecting to FTP")
with FTP("localhost") as ftp:

    ftp.login()

    # Grabs all files in specified dir
    file_list = ftp.nlst("/")

    # Compiles a regex that matches the file name format.
    # YYYYMMDDHHMMSS is exactly 14 digits of 1-9 with MED_DATA_ before and .csv after
    # It's case-insensitive so MeD_DaTA_ and .Csv would be allowed
    
    # TODO: More specific to time and date digit limits
    pattern = re.compile("(?i)(MED_DATA_)([0-9]{14})\.(csv)")

    for file_name in file_list:
        if (pattern.match(file_name)):
            print(f"Found valid medical data: {file_name}")
            formatted_file_name = file_name.upper()
            with open(os.path.join("ftp-download-test", formatted_file_name), "wb") as f:
                ftp.retrbinary(f"RETR {file_name}", f.write)