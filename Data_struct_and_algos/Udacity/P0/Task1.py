"""
Read file into texts and calls.
It's ok if you don't understand how to read files.
"""
import csv
with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)


"""
TASK 1:
How many different telephone numbers are there in the records? 
Print a message:
"There are <count> different telephone numbers in the records."
"""

all_diff_number = []

# This loop through all numbers in calls and select the distinct number
# It adds the distinct number to a list
for row in calls:
    if row[0] not in all_diff_number:
        all_diff_number.append(row[0])
    if row[1] not in all_diff_number:
        all_diff_number.append(row[1])

# This loops through all number in text and it select the distinct
for row in texts:
    if row[0] not in all_diff_number:
        all_diff_number.append(row[0])
    if row[1] not in all_diff_number:
        all_diff_number.append(row[1])

print(f"There are {len(all_diff_number)} different telephone numbers in the records")

