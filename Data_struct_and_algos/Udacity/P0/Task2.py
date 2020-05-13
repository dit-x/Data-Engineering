"""
Read file into texts and calls.
It's ok if you don't understand how to read files
"""
import csv
with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)

"""
TASK 2: Which telephone number spent the longest time on the phone
during the period? Don't forget that time spent answering a call is
also time spent on the phone.
Print a message:
"<telephone number> spent the longest time, <total time> seconds, on the phone during 
September 2016.".
"""

duration = 0

# Loop through all rows in calls

telephone_duration = {}
all_diff_number = []
for row in calls:

    # I made a list "all_diff_number" if the telephone number has been checked
    # If not, add telephone number to the list, this is to ensure with have unique number
    if row[0] not in all_diff_number:
        telephone_duration[row[0]] = int(row[3])
        all_diff_number.append(row[0])

    # if phone number already exist, add next duration to the previous duration
    else:
        telephone_duration[row[0]] = telephone_duration[row[0]] + int(row[3])

        
max_time = 0
for telephone, duration in telephone_duration.items():

    # check condition
    if duration > max_time: 
        telephone, max_time = telephone, duration


print(f"{telephone} spent the longest time, {max_time} seconds, on the phone during September 2016.")

# 46232
