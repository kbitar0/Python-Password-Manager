from cryptography.fernet import Fernet
import os

file = open('passwords.txt','a')
keyfile = open('key.key','a')
mkeyfile = open('mkey.key','a')
file.close()
keyfile.close()
mkeyfile.close()

def writekey():
    key = Fernet.generate_key()
    with open('key.key','wb') as key_file:
        key_file.write(key)

def writemasterkey():
    key = Fernet.generate_key()
    with open('mkey.key','wb') as key_file:
        key_file.write(key)

def createpassword():
    mpassword = input('What would you like your master password to be?  ')
    with open('passwords.txt','a') as f:
        f.write(mfer.encrypt(mpassword.encode()).decode() +'\n')

def retrieve_mkey():
    with open("mkey.key","rb") as r:
        mkey = r.read()
    return mkey

def retrieve_key():
    with open("key.key","rb") as r:
        key = r.read()
    return key

if os.path.getsize('key.key') == 0:
    writekey()

if os.path.getsize('mkey.key') == 0:
    writemasterkey()

mkey = retrieve_mkey()
mfer = Fernet(mkey)

if os.path.getsize('passwords.txt') == 0:
    createpassword()

mpass = input("Enter your master password:  ")
key = retrieve_key() + mpass.encode()
fer = Fernet(key)

def view():
    with open('passwords.txt', 'r') as f:
        for line in f.readlines()[1:]:
            info = line.rstrip()
            user, passw = info.split('|')
            print(f'User: {user} \nPassword: {fer.decrypt(passw.encode()).decode()} \n')

def new():
    uname = input('Account username:')
    password = input('Account password:')
    with open('passwords.txt', 'a') as f:
        f.write(uname + "|" + fer.encrypt(password.encode()).decode() + "\n")


if os.path.getsize('passwords.txt') > 0:
    with open('passwords.txt','r') as f:
        lines = f.readlines()
        x = lines[0]
    if mpass == mfer.decrypt(x.encode()).decode():

        while True:
            opt = input('Are you trying to add a new password or view existing ones (Enter either view or new, or type "esc" to leave:  ').lower()
            if opt == "esc":
                break
            if opt == "view":
                view()
            elif opt == "new":
                new()
            else:
                print('Invalid input.')
    else:
        print('Incorrect password, program will end.')
