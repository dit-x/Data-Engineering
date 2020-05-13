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
TASK 4:
The telephone company want to identify numbers that might be doing
telephone marketing. Create a set of possible telemarketers:
these are numbers that make outgoing calls but never send texts,
receive texts or receive incoming calls.

Print a message:
"These numbers could be telemarketers: "
<list of numbers>
The list of numbers should be print out one per line in lexicographic order with no duplicates.
"""

# get the distinct number in the calling number column of calls
calling_number = set([x[0] for x in calls])


# Hold all numbers in send texts, receive texts or receive incoming calls column
nor_telemarket_number = []

# Get the distinct number from the receiving column of calls
for row in calls:
    if row[1] not in nor_telemarket_number:
        nor_telemarket_number.append(row[1])


# get the distinct number from texts
for row in texts:
    if row[0] not in nor_telemarket_number:
        nor_telemarket_number.append(row[0])
    if row[1] not in nor_telemarket_number:
        nor_telemarket_number.append(row[1])


telemarket_number = []
count = 0
print("These numbers could be telemarketers: ")

# Remove all telephone number in calling_number and nor_telemarket_number
for what in sorted(calling_number):

    if what in nor_telemarket_number:
        continue
    count += 1
    print(what)
    telemarket_number.append(what)
