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
TASK 0:
What is the first record of texts and what is the last record of calls?
Print messages:
"First record of texts, <incoming number> texts <answering number> at time <time>"
"Last record of calls, <incoming number> calls <answering number> at time <time>, lasting <during> seconds"
"""

first_text = texts[1]
last_call = calls[-1]

print(f'First record of texts, "{first_text[0]}" texts "{first_text[1]}" at time {first_text[2]}')

print(f'Last record of calls, "{last_call[0]}" calls "{last_call[1]}" at time {last_call[2]}, lasting {last_call[3]} seconds')
