character = ["0", "1","2","3","4","5","6","7","8", 
"9","A","B","C","D","E","F"]

numberToConvert = int(input("Enter number to convert: "))

hold = numberToConvert

base = int(input("To what base? "))

convertedNumber = []

while numberToConvert != 0:
	a = numberToConvert % base
	numberToConvert //= base
	convertedNumber.append(character[a])

print("{} in decimal is converted to base {}, it is:".format(hold, base), end = ' ')

convertedNumber.reverse()
for digit in convertedNumber:
	print(digit, end = '')