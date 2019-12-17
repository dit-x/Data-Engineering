import csv

def user(username):

    with open('user_details.txt', 'r') as f:
        f_content = csv.DictReader(f)

        for line in f_content:
            if line["username"].lower() == username.lower():
                print(f"\nHello, {line['firstName'].title()} {line['lastName'].title()}")
                print(f"""Here are your information: 
    Username: {username}
    University: {line['university'].upper()}
    Email: {line['email']}""")

                break



def newUser(fName, lName, university, email, username):

    with open('user_details.txt', 'a') as f:
        f.write(f"\n{fName},{lName},{university},{email},{username}")
        print("********Acoount created**********")


def checkUsername(response):
    while True:
        check = ''
        username = input("Enter username: ")
        username = username.lower()

        with open('user_details.txt', 'r') as f:
            f_content = csv.DictReader(f)

            for line in f_content:
                a =line['username']
                a = a.lower()

                if username == a and response == "sign in":
                    check = "yes"
                    print("\n\t******Signed in*******")
                    break

                elif username == a and response == "sign up":
                    check = "sign in"
                    print("Username taken, input again")
                    break

        if check != 'sign in':

            break

    return username


def checkEmail():
    while True:
        check = ''
        email = input("Enter your mail: ")
        email = email.lower()
        with open('user_details.txt', 'r') as f:
            f_content = csv.DictReader(f)

            for line in f_content:
                a =line['email'].lower()

                if email == a:
                    check = "yes"
                    print("The email has been used, enter another one")
                    break

        if check != 'yes':
            print("Valid email!")
            break

    return email


def signUp():
    fName = input("\nEnter fist name: ")
    lName = input("Enter last name: ")
    university = input("Enter university: ")
    email = checkEmail()
    username = checkUsername("sign up")

    newUser(fName, lName, university, email, username)

def signIn():
    username = checkUsername("sign in")

    user(username)


print("Welcome to this new code test")
print("-----------------------------")

sign = input("Do you have an account with us? (y/n): ")

if sign == 'y':
    signIn()
else:
    sign = input("Do you want to join? (y/n): ")
    if sign == 'y':
        signUp()
    else:
        print("We hope you change your mind")
