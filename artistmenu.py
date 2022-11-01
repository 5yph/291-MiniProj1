import sqlite3

def artistMenu(aid, con, cur):
    global connection, cursor

    connection = con
    cursor = cur

    print("")
    print("Artists")
    print("---------")

    t = (aid,)
    cursor.execute('SELECT name FROM artists WHERE artists.aid=?;', t)
    name = cursor.fetchone()

    print("Welcome {}! What would you like to do?".format(name[0]))
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
            print("---------")
            print("Adding a song !")
            # add a song here
            addSong(aid)
        elif (x == '2'):
            print("Finding top fans !")
        elif (x == '3'):
            print("Finding top playlists !")

def addSong(aid):
    # connection = con
    # cursor = cur
    global connection, cursor 

    # get new song id (1 + highest song id)
    cursor.execute('SELECT MAX(sid) FROM songs;')
    highest_sid = cursor.fetchone()

    print(highest_sid[0])

    # ask for song title and duration


    # fcheck if song already exists


    # add song


    # add perform


    # ask for  other artists who may be involved


    # add those if it's the case

    print("")
