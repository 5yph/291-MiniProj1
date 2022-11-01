import sqlite3
import time

def userMenu(uid, con, cur):
    global connection, cursor

    connection = con
    cursor = cur

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
