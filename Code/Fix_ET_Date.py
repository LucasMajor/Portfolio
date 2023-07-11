##Data Cleaning File##
##This script is used to fix a date string discrepency between the daily ET data and Phase II data.
## This allows us to join the two data sets in later R analysis.

##This program works by reading in the daily ET data,
## and adjusting the date string format to match the Phase II data's format.
## ET date format: %M/%d/%yyyy ; PhaseII date format: %MM/%dd/%yy
##  ET date has no leading zeros with month and day, and 4 digit year instead of 2 digit.

import csv
newdat = []
header = []

#Read data with csv
path_to_input_file = r"2022_TROE Daily ET Export.csv"

with open(path_to_input_file, 'r') as file:
  csvreader = csv.reader(file)
  #pull header for later use. assumes header starts with "Date"
  for row in csvreader:
    if (row[0][0] == "D"):
        header.append(row)
    else: #Adjusts date based on basic string location checks
        datestring = row[0]
        if row[0][0] == '1':
            pass
        else:
            datestring = '0' + row[0]
        if datestring[4] == '/':
            datestring = datestring[0:3] + '0' + datestring[3:]

        datestring = datestring[0:6] + datestring[8:]
        row[0] = datestring
        newdat.append(row)

#Write to new file
path_to_output_file = r"ET_FIXED_DATE.csv"
with open(path_to_output_file, 'w', newline = '') as file:
    filewriter = csv.writer(file, delimiter = ',')
    filewriter.writerow(header[0])
    for i in range(len(newdat)):
        thisrow = newdat[i]
        filewriter.writerow(thisrow)
