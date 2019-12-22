

def numToWord(number):
	character = ["zero", "one", "two","three","four","five", "six", "seven", "eight","nine"]

	store = []

	print("\nIf {} is coverted to word, it is: \n" .format(number) )

	while number != 0:
		a = number % 10 #store the remainder in a
		number //=  10 #divide number by 10
		store.append(character[a]) #put the reminder in store
	
	store.reverse() #this is to reverse store element

	for word in store:
		print(word, end = ' ')

numbers = int(input("Enter number: "))
numToWord(numbers)