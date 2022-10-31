import sqlite3
import sys
from getpass import getpass
import time

import MySQLdb

connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

def verifyID(id):
    global connection, cursor

    # Get user id if exists
    id1 = (id,)
    cursor.execute('SELECT uid FROM users WHERE uid=?;', id1)
    uid = cursor.fetchone()
    if (uid is None):
        uid = 0
    # Get artist id if exists
    cursor.execute('SELECT aid FROM artists WHERE aid=?;', id1)
    aid = cursor.fetchone()
    if (aid is None):
        aid = 0

    # If the ID is in both user and artist
    if uid != 0 and aid != 0:
        return 3, uid, aid
    ## If the ID is only in user
    elif uid != 0:
        return 1, uid
    # If the ID is only in artist
    elif aid != 0:
        return 2, aid
    # Not found
    else:
        return 0

def login(logintype, id, password):
    global connection, cursor
    t = (id, password,)

    # Return 1 if the password is found, otherwise 0
    if (logintype == 1):
        cursor.execute('SELECT uid FROM users WHERE uid=? AND pwd=?;', t)
        if (cursor.fetchone() is not None):
            return 1
        else:
            return 0
    if (logintype == 2):
        cursor.execute('SELECT aid FROM artists WHERE aid=? AND pwd=?;', t)
        if (cursor.fetchone() is not None):
            return 1
        else:
            return 0

def register(id, name, password):
    global connection, cursor    
    cursor.execute('INSERT INTO users VALUES (?,?,?)', (id, name, password))
    connection.commit()

def loginScreen():
    id = None
    type = None
    while (1):
        print("")
        print("Welcome to ProjectCloud, please login ! ! !")
        print("-------------------------------------------")
        print("1: Login")
        print("2: Register")
        print("3: Exit")
        print("")

        x = input()
        if (x == '1'):
            print("LOGIN")
            print("----------")
            print("ID:")
            id = input()
            verify = verifyID(id) # analyzes user ID if it exists or not
            if (verify == 0):
                # no valid id
                print("Could not find login! ! ! Please register ! ! !")
                continue
            elif(verify[0] == 3):
                # id in users and artists
                print("Found login in Users and Artists !")
                print("What would you like to login as? User or Artist?")
                while (1):
                    y = input()
                    if (y.lower() == 'user'):
                        type = 1
                        break
                    elif(y.lower() == 'artist'):
                        type = 2
                        break
                    else:
                        print("Type either 'User' or 'Artist' !")
            elif(verify[0] == 1):
                # user
                print("User Login...")
                type = 1
            elif(verify[0] == 2):
                # artist
                print("Artist Login...")
                type = 2

            password = getpass("Password: ")

            # attempt to login
            if (login(type, id, password) != 0):
                return type, id
            else:
                print("Invalid Password !")
                continue

        elif(x == '2'):
            print("REGISTER")
            print("--------")
            print("Desired User ID:")
            id = input()
            if (id[0] != 'u' or not id[1:].isnumeric()):
                print("Enter a valid User ID ! Format 'u' then an integer !")
                continue
            elif (verifyID(id) != 0):
                print("That ID exists ! Please choose another !")
                continue
            print("Your Name:")
            name = input()
            password = getpass("Password: ")
            if (len(name) == 0 or len(password) == 0):
                print("Please use valid entries !")
                continue
            register(id, name, password)
            return 1, id
            
        elif(x == '3'):
            print("Exiting ! Thanks for using ProjCloud, the worst streaming service !")
            break

        else:
            print("Select a valid option ! ! !")

def addSession(uid):
    global connection, cursor
    cur_date = time.strftime("%Y-%m-%d %H:%M:%S")
    t = (str(uid),)
    cursor.execute('SELECT MAX(sno+0) FROM sessions WHERE uid=?;', t)
    sno = cursor.fetchone()
    if (sno[0] is None):
        sno = 1
    else:
        sno = sno[0] + 1
    cursor.execute('INSERT INTO sessions VALUES (?,?,?,?)', (uid, sno, cur_date, None))
    connection.commit()
    return sno

def endSession(uid, sno):
    global connection, cursor
    end_date = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('UPDATE sessions SET end = ? WHERE uid = ? AND sno = ?', (end_date, uid, sno))
    connection.commit()

def userMenu(uid):
    print("")
    print("USER MENU")
    print("---------")
    print("Welcome ! What would you like to do?")
    sno = None
    while (1):
        print("1: Start a listening session !")
        print("2: Search for songs and playlists !")
        print("3: Search for artists !")
        print("4: End your session !")
        print("5: Logout !")
        x = input()
        if (x not in ['1','2','3','4','5']):
            print("Please put a valid input !")
            continue
        if (x == '5'):
            print("Logging out !")
            break
        elif (x == '1'):
            print('Starting a session !')
            if (sno is not None):
                print("You're already listening ! End this session first !")
                continue
            sno = addSession(uid)
        elif (x == '4'):
            if (sno is None):
                print("You don't have a session !")
                continue
            else:
                endSession(uid, sno)
                sno = None

def main():
    global connection, cursor
    db = "./" + str(sys.argv[1])
    connect(db)
    while (1):
        x = loginScreen() # interface for logging in 
        # doube check if x is a list or is just the first of the returned types
        if (x is not None):
            if (x[0] == 1):
                print("Login Type User")
            else:
                print("Login Type Artist")
            print("Successfully logged in as: " + x[1])
        else:
            break

        # More features past this point.

        #User Menu
        if (x[0] == 1):
            userMenu(x[1])
        else:
            print("")

    connection.close()

if __name__ == "__main__":
    main()
