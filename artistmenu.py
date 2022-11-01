import sqlite3

def artistMenu(aid, con, cur):
    global connection, cursor

    connection = con
    cursor = cur

    print("")
    print("ARTISTS MENU")
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

    new_sid = highest_sid[0] + 1

    # ask for song title and duration
    song_title = input("Enter song title (string): ")
    song_dur = input("Enter song duration (integer): ")

    # check if duration is integer
    if not song_dur.isdigit():
        print("Error: duration is not an integer")
        print("Exiting to menu...")

    # account for case insensitivity -> turn everything lower case
    song_title = song_title.lower()

    # check if song already exists
    song_exist_query = '''
                    SELECT songs.sid
                    FROM songs, perform, artists
                    WHERE perform.aid = artists.aid
                    AND perform.sid = songs.sid
                    AND artists.aid=?
                    AND songs.title=?
                    AND songs.duration=?;
                '''
    t = (aid, song_title, song_dur,)
    cursor.execute(song_exist_query, t)

    song_exit_rows = cursor.fetchall()
    print(song_exit_rows)
    # if so, warn user and either reject it or confirm addition of new song
    if len(song_exit_rows) > 0:
        # row exists matching song description
        print("Song already exists with sid: " + str(song_exit_rows[0][0]))
        
        print("Add song anyway?")
        print("1: Yes")
        print("2: No")

        ans = input()

        if (ans == '2'):
            print("Not adding song...")
            return
        elif (ans != '1'):
            print("Invalid selection, returning to menu")
            return

    # add song to songs table
    cursor.execute('INSERT INTO songs VALUES (?,?,?)', (new_sid, song_title, song_dur))
    connection.commit()

    # add perform
    cursor.execute('INSERT INTO perform VALUES (?,?)', (aid, new_sid))
    connection.commit()

    print("Currently added song: " + song_title + " of duration " + str(song_dur) + " with id: " + str(new_sid))
    print("Artist with aid: " + aid + " performs this song")

    while(1):
        # ask for other artists who may be involved
        print("Add additional artists who performed this song? (Only artists that exist in the database may be added)")
        print("1: Yes")
        print("2: No")

        ans = input()

        if (ans == '1'):
            # add other artists


            print("")
        elif (ans == '2'):
            break
        else:
            print("Invalid selection, try again.")


    return
