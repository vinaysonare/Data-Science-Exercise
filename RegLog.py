# Guvi Task-2, Assignment-1
# Registration and Login system with Python, file handling
from pymongo import MongoClient


def main():
    client = MongoClient(
        'mongodb://login_authenticator:welcome12345@clustur0-shard-00-00.iwdrc.mongodb.net:27017,'
        'clustur0-shard-00-01.iwdrc.mongodb.net:27017,'
        'clustur0-shard-00-02.iwdrc.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-hrd65f-shard-0'
        '&authSource=admin&retryWrites=true&w=majority')
    db = client['User_Data']
    col = db['User_Credentials']

    option = int(input('Please enter an option:\n1 for Registration.\n2 for Log In.\n3 for Forgot Password.\n'))
    username = input('User Name: ')
    if not validate_id(username):
        print('invalid User Name')
        return
    password = ''
    if option != 3:
        password = input('Password: ')
        if not validate_pass(password):
            return
    # Registration
    if option == 1:
        if col.count_documents({'username': username}) > 0:
            print("User Already exist: ")
        else:
            col.insert_one({'username': username, 'password': password})
            print('Registered Successfully!')
    # Log In
    elif option == 2:
        if col.count_documents({'username': username}) == 0:
            reg = input("User doesn't exist!!! Do you want to register? (Y or N): ")
            if reg.upper() == 'Y':
                col.insert_one({'username': username, 'password': password})
                print('Registered Successfully!')
            else:
                return
        else:
            x = col.find_one({'username': username})
            if password == x['password']:
                print('Logged In Successfully !!!')
            else:
                print('Incorrect Password !!!')

    # Forgot Password
    elif option == 3:
        x = col.find_one({'username': username})
        print('Password is: ' + x['password'])
    else:
        print('Invalid option')


def validate_id(username):
    for i in range(len(username)):
        if username[i] == '@' and username[i + 1] == '.':
            return False
    if 65 <= ord(username[0]) <= 90 or 97 <= ord(username[0]) <= 122 or 48 <= ord(username[0]) <= 57:
        return True
    else:
        return False


def validate_pass(password):
    # getting counts
    spch = 0
    dgt = 0
    upcase = 0
    locase = 0
    for ch in password:
        if 65 <= ord(ch) <= 90:
            upcase += 1
        elif 97 <= ord(ch) <= 122:
            locase += 1
        elif 48 <= ord(ch) <= 57:
            dgt += 1
        else:
            spch += 1
    if len(password) < 5 or len(password) > 16:
        print('Password length should be between 5 and 16.')
        return False
    elif upcase == 0 or locase == 0 or dgt == 0 or spch == 0:
        print('Password must have at least one special character, one digit, one uppercase and one lowercase character')
        return False
    else:
        return True


main()
