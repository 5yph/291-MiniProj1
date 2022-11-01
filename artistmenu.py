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
        print("Select an option: ")
        print("1: Add a song !")
        print("2: Find top fans & playlists!")
        print("3: Logout !")
        x = input()
        if (x not in ['1','2','3']):
            print("Please put a valid input !")
            continue
        if (x == '3'):
            print("Logging out !")
            break
        elif (x == '1'):
            print("---------")
            print("Adding a song !")
            # add a song here
            addSong(aid)
        elif (x == '2'):
            print("---------")            
            print("Finding top fans & playlists!")
            findTopStats(aid)

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

    while(1):
        song_dur = input("Enter song duration (integer): ")

        # check if duration is integer
        if not song_dur.isdigit():
            print("Error: duration is not an integer")
        else:
            break

    # account for case insensitivity -> turn everything lower case
    song_title_lower = song_title.lower()

    # check if song already exists
    song_exist_query = '''
                    SELECT songs.sid
                    FROM songs, perform, artists
                    WHERE perform.aid = artists.aid
                    AND perform.sid = songs.sid
                    AND LOWER(artists.aid)=?
                    AND LOWER(songs.title)=?
                    AND songs.duration=?;
                '''
    t = (aid, song_title_lower, song_dur,)
    cursor.execute(song_exist_query, t)

    song_exist_rows = cursor.fetchall()
    print(song_exist_rows)
    # if so, warn user and either reject it or confirm addition of new song
    if len(song_exist_rows) > 0:
        # row exists matching song description
        print("Song already exists with sid: " + str(song_exist_rows[0][0]))
        
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

    artists_who_perform = set() # maintain set of all aids who performed this song
    artists_who_perform.add(aid.lower())

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

            # get all artist info
            new_artist_aid = input("Input artist aid: ")

            if(new_artist_aid.lower() in artists_who_perform):
                print("Error: This artist is already performing this song!")
                continue

            # find if this artist exists

            aid_exist_query = '''
                SELECT artists.aid
                FROM artists
                WHERE artists.aid=?;
            '''
            t = (new_artist_aid.lower(),)
            cursor.execute(aid_exist_query, t)

            aid_exist_rows = cursor.fetchall()
            if len(aid_exist_rows) == 0:
                print("ERROR: artist id not in database, will not add")
            else:
                cursor.execute('SELECT artists.aid, artists.name FROM artists WHERE LOWER(artists.aid)=?', t)
                artist_info = cursor.fetchone()

                print(artist_info)

                print("Artist info: " + str(artist_info))
                print("Confirm add?")
                print("1: Yes")
                print("2: No")
                ans2 = input()

                if (ans2 == '1'):
                    # add to perform
                    cursor.execute('INSERT INTO perform VALUES (?,?)', (new_artist_aid, new_sid))
                    connection.commit()
                    artists_who_perform.add(new_artist_aid.lower())
                else:
                    print("Not adding this artist...")

        elif (ans == '2'):
            break
        else:
            print("Invalid selection, try again.")

    return

def findTopStats(aid):

    # get top users
    get_top_fans_query = '''
                    SELECT l.uid, u.name
                    FROM listen l, songs s, perform p, users u
                    WHERE l.sid=s.sid 
                    AND s.sid=p.sid
                    AND u.uid = l.uid
                    AND p.aid=?
                    group by l.uid
                    order by sum(l.cnt*s.duration) desc
                    limit 3;
                    '''
    
    t = (aid.lower(),)
    cursor.execute(get_top_fans_query, t)

    # songs is a list of tuples where the first index of each tuple is the song id
    top_fans = cursor.fetchall()

    print("Top fans:")
    for i, fan in enumerate(top_fans):
        print("Fan #" + str(i+1) + ": " + fan[0] + " -- " + fan[1])

    '''
    for song in songs:
        print(song[0]) 
    '''

    # listen.cnt * songs.duration will return the total amount of time
    # a user has listened to this song


    return