import sqlite3
import time

global connection, cursor

def artistMenu(aid, con, cur):
    connection = con
    cursor = cur

    print("")
    print("Artists")
    print("---------")
    print("Welcome ! What would you like to do?")
    sno = None
    while (1):
        print("1: Add a song !")
        print("2: Find top fans !")
        print("3: Find top playlists !")
        print("4: Logout !")
        x = input()
        if (x not in ['1','2','3','4']):
            print("Please put a valid input !")
            continue
        if (x == '4'):
            print("Logging out !")
            break
        elif (x == '1'):
            print("Adding a song !")
            # add a song here
        elif (x == '2'):
            print("Finding top fans !")
        elif (x == '3'):
            print("Finding top playlists !")