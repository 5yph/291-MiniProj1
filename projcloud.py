import sqlite3
import sys
from getpass import getpass
from usermenu import userMenu
from artistmenu import artistMenu

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

    # id passed is lower case, account for this in database

    # Get user id if exists
    id1 = (id,)
    cursor.execute('SELECT uid FROM users WHERE uid=LOWER(?);', id1)
    uid = cursor.fetchone()
    if (uid is None):
        uid = 0
    # Get artist id if exists
    cursor.execute('SELECT aid FROM artists WHERE aid=LOWER(?);', id1)
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
        cursor.execute('SELECT uid FROM users WHERE LOWER(uid)=? AND pwd=?;', t)
        if (cursor.fetchone() is not None):
            return 1
        else:
            return 0
    if (logintype == 2):
        cursor.execute('SELECT aid FROM artists WHERE LOWER(aid)=? AND pwd=?;', t)
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
            id = input().lower()
            verify = verifyID(id) # analyzes user ID if it exists or not

            if (verify == 0):
                # no valid id
                print("Could not find login! ! ! Please register ! ! !")
                continue
            elif(verify[0] == 3):
                # id in users and artists
                print("Found login in Users and Artists !")
                print("What would you like to login as? User or Artist?")
                print("Type either 'User' or 'Artist' !")
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
            id = input().lower()
            verify = verifyID(id)

            if (len(id) > 4):
                print("Enter a valid User ID ! At most 4 characters !")
                continue
            elif (verify != 0):
                print("That User ID exists ! Please choose another !")
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

def main():
    global connection, cursor
    if (len(sys.argv) != 2):
        print("Input the database !")
        return
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

        if (x[0] == 1):
            #User Menu
            userMenu(x[1], connection, cursor)
        elif (x[0] == 2):
            # artist menu
            artistMenu(x[1], connection, cursor)

    connection.close()

if __name__ == "__main__":
    main()
