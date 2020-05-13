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
TASK 3:
(080) is the area code for fixed line telephones in Bangalore.
Fixed line numbers include parentheses, so Bangalore numbers
have the form (080)xxxxxxx.)

Part A: Find all of the area codes and mobile prefixes called by people
in Bangalore.
 - Fixed lines start with an area code enclosed in brackets. The area
   codes vary in length but always begin with 0.
 - Mobile numbers have no parentheses, but have a space in the middle
   of the number to help readability. The prefix of a mobile number
   is its first four digits, and they always start with 7, 8 or 9.
 - Telemarketers' numbers have no parentheses or space, but they start
   with the area code 140.

Print the answer as part of a message:
"The numbers called by people in Bangalore have codes:"
 <list of codes>
The list of codes should be print out one per line in lexicographic order with no duplicates.

Part B: What percentage of calls from fixed lines in Bangalore are made
to fixed lines also in Bangalore? In other words, of all the calls made
from a number starting with "(080)", what percentage of these calls
were made to a number also starting with "(080)"?

Print the answer as a part of a message::
"<percentage> percent of calls from fixed lines in Bangalore are calls
to other fixed lines in Bangalore."
The percentage should have 2 decimal digits
"""

# Add a field name to the calls list
call_fields_name = ["calling number", "receiving number", "timestamp", "duration"]
calls.append(call_fields_name)

# Make a dictionary from the list using the fieldname (last element) as the key
dict_calls = {a[-1]: (a[:-1]) for a in zip(*calls)}

count_all = 0
count_bangalore = 0
called_by_bangalore = []


# I used enumerate to get the value and the location (number)
for index, value in enumerate(dict_calls["calling number"]):
   
    if "(080)" == value[:5]:
        count_all += 1
        received_from_bangalore = dict_calls["receiving number"][index]

        if "(080)" == received_from_bangalore[:5]:
          count_bangalore += 1

    # Manipulating the telephone to get area code and the mobile prefixes
    if ' ' in value:
        area_code = value[:4]

    elif '(' in value:
        for i, string in enumerate(value):
            if string == ")":
                break
        area_code = value[:i+1]

    else:
        area_code = "140"


    if area_code not in called_by_bangalore:     
        called_by_bangalore.append(area_code)

print("The numbers called by people in Bangalore have codes:")

for code in sorted(called_by_bangalore):
    print(code)


percent = count_bangalore / count_all * 100

print("\n{0:.2f} percent of calls from fixed lines in Bangalore \
are calls to other fixed lines in Bangalore.".format(percent))