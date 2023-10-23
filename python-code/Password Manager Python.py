import os
from cryptography.fernet import Fernet

def write_key(filename):
    key = Fernet.generate_key()
    with open(filename, 'wb') as key_file:
        key_file.write(key)

def retrieve_key(filename):
    with open(filename, 'rb') as key_file:
        return key_file.read()

def create_master_password(mfer):
    mpassword = input('Set your master password: ')
    with open('passwords.txt', 'a') as f:
        f.write(mfer.encrypt(mpassword.encode()).decode() + '\n')

def check_master_password(mfer):
    with open('passwords.txt', 'r') as f:
        stored_pass = f.readline().strip()
    mpass = input("Enter your master password: ")
    return mfer.decrypt(stored_pass.encode()).decode() == mpass

def view_passwords(fer):
    with open('passwords.txt', 'r') as f:
        for line in f.readlines()[1:]:
            user, passw = line.rstrip().split('|')
            print(f'User: {user} \nPassword: {fer.decrypt(passw.encode()).decode()} \n')

def add_password(fer):
    uname = input('Account username: ')
    password = input('Account password: ')
    with open('passwords.txt', 'a') as f:
        f.write(uname + "|" + fer.encrypt(password.encode()).decode() + "\n")

def main():
    if not os.path.exists('key.key'):
        write_key('key.key')

    if not os.path.exists('mkey.key'):
        write_key('mkey.key')

    mkey = retrieve_key('mkey.key')
    mfer = Fernet(mkey)

    if not os.path.exists('passwords.txt') or os.path.getsize('passwords.txt') == 0:
        create_master_password(mfer)

    if check_master_password(mfer):
        key = retrieve_key('key.key')
        mpass = input("Re-enter your master password for verification: ")
        fer = Fernet(key + mpass.encode())

        while True:
            opt = input('Choose an action (view/new/esc): ').lower()
            if opt == "esc":
                break
            elif opt == "view":
                view_passwords(fer)
            elif opt == "new":
                add_password(fer)
            else:
                print('Invalid input.')
    else:
        print('Incorrect master password. Exiting.')

if __name__ == '__main__':
    main()

