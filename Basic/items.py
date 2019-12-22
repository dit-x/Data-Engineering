
"""                THIS LIST IS CREATED USING DICTIONARY, MORE COMPLICATED
                        BUT USEFUL FOR DICTIONARY UNDERSTANDING"""

item = {} # the main dict of this program
i =1

while i<=2:
    item[i] = {} # Make a dict in a dict to store the name and price
                 # Note that this new dict is the value in item dict ( the main dict body)
                 # from the declaration we have in item_dict
                 # {i: {'name' : inputtedName, 'price' : inputted_price}

    item[i]['name'] = input("Enter item name: ") # key is name, value is the input

    if item[i]['name'] == "stop" or item[i]['name'] == "Stop":
        del item[i]
        break



    item[i]['price'] = int(input("Enter item price: ")) # key is price, value is the input
    i += 1

# print out item with the price tag
for d in item.keys():
    for key,value in item[d].items():
        print(f".....{key} : {value}")
    print()




#
# """             THIS IS DONE USING LIST, THIS IS QUITE SIMPLER THAN THE DICTIONARY
#                         ONE, THIS ALSO HELP TO UNDERSTAND LIST                              """
#
# allItems = []
# i =1
# item = {}
#
# while i<=2:
#
#     item['name'] = input("Enter item name: ") # create a new dict to store
#                                               # with key "NAME" and value "USER_INPUT"
#
#     if item['name'] == "stop" or item['name'] == "Stop":
#         del item
#         break
#
#     item['price'] = int(input("Enter item price: ")) # create a new dict to store
#                                                      # with key "NAME" and value "USER_INPUT"
#
#
#     """ The item has two dictionary to store in allItems list before looping tru again
#         i.e item = {'name': 'USER_INPUT', 'price': USER_INPUT} """
#
#     allItems.append(item)
#     i += 1
#
# print("\n")
#
# print(allItems,"\n\n") # Check what in list
#
# # print out item with price tag
# for element in allItems:
#     for key,value in element.items():
#          print(f".....{key} : {value}")

