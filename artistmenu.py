import sqlite3
import time

def userMenu(uid, con, cur):

    global connection, cursor, songCursor

    connection = con
    cursor = cur

    # user menu interface
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
            # invalid input
            print("Please put a valid input !")
            continue
        if (x == '5'):
            # logout (close any sessions first)
            if (sno is not None):
                print("Closing current session before logout...")
                endSession(uid, sno)

            print("Logging out !")
            break
        elif (x == '1'):
            # start sessions
            print('Starting a session !')
            if (sno is not None):
                print("You're already listening ! End this session first !")
                continue
            sno = addSession(uid)
        elif (x == '2'):
            # search songs for keywords
            print("Enter space separated keywords you'd like to search by ! (e.g 'Fun Songs')")
            keywords = input()
            if keywords == '':
                print("Enter an input properly !")
                continue
            # get song results
            results = spSearch(keywords)
            if len(results) > 5:
                # display only first 5
                for i in range(5):
                    print(results[i][0] + ", " + results[i][1] + ", " + results[i][2]) #if you want the # of matches, use [3]
                print("There are more than 5 matches ! Do you want to see the rest ? ! ?")
                y = input('Y or N: ')
                if (y.upper() == 'Y'):
                    print('Showing all results ! :')
                    for result in results:
                        print(result[0] + ", " + result[1] + ", " + result[2])
                elif (y.upper() == 'N'):
                    print('Oh well whatever !')
                else:
                    print("Y or N bozo ! You don't get to see the rest then !")
            else:
                # display all if less than 6
                for result in results:
                    print(result[0] + ", " + result[1] + ", " + result[2])
                    
            while(1):
                # song actions
                print("Select a song to start performing actions (Give sid). Or, if you want to select a playlist, enter 'P(PID)'. ex: playlist with PID:0, enter 'P0'. Enter 'q' to quit.")

                songSelected = input().lower()

                if songSelected == "":
                    print("Please give an input.")
                    continue
                elif songSelected == 'q':
                    print("Exiting:")
                    break
                elif songSelected[0] == 'p':
                    hasPlaylist = 0
                    for result in results:
                        if result[0][0].lower() == 'p' and songSelected[1:] == result[0][13:]:
                            hasPlaylist = hasPlaylist + 1
                            playlists = getSongsPlaylist(songSelected[1])
                            while(1):
                                for result in playlists:
                                    print(result[0] + ", " + result[1] + ", " + result[2])
                                print("Select a song to start performing actions (Give sid). Enter 'q' to quit.")

                                songSelected = input()

                                if songSelected == "":
                                    print("Please give an input.")
                                    continue
                                elif songSelected == 'q':
                                    print("Exiting:")
                                    break
                                foundSong = 0
                                for resultSong in playlists:
                                    if songSelected == resultSong[0][9:]:
                                        foundSong = foundSong + 1
                                        sno = songActions(uid, sno, songSelected)
                                        break
                                if foundSong == 0:
                                    print("Song/Playlist not found. Please enter a proper ID within the list of songs/playlists returned.")
                                continue
                            break
                else:
                    foundSong = 0
                    for resultSong in results:
                        if songSelected == resultSong[0][9:]:
                            foundSong = foundSong + 1
                            sno = songActions(uid, sno, songSelected)
                            break
                    if foundSong == 0:
                        print("Song not found. Please enter a proper ID within the list of songs returned.")
                    continue
            print("")

        elif (x == '3'):
            print('Provide a keyword for artist name, or song they performed, seperated by space:')
            keywords = input()
            results = findArtist(keywords)
            if keywords == '':
                print("Please give an input.")
                continue
            if len(results) > 5:
                ind = 0
                for i in range(5):
                    print("Index: " + str(ind) + " " + results[i][0] + ", " + results[i][1] + ", " + results[i][2]) #if you want the # of matches, use [3]
                    ind = ind + 1
                print("There are more than 5 matches ! Do you want to see the rest ? ! ?")
                y = input('Y or N: ')
                if (y.upper() == 'Y'):
                    print('Showing all results ! :')
                    i - 0
                    ind = 0
                    for result in results:
                        print(" Index: " + str(ind) + " " + result[0] + ", " + result[1] + ", " + result[2])
                        i = i + 1
                        ind = ind + 1
                elif (y.upper() == 'N'):
                    print('Not displaying all the results')
                else:
                    print("Please select Y or N.")

            elif len(results) > 0:
                i = 0
                for result in results:
                    print(" Index: " + str(i) + " " +  result[0] + ", " + result[1] + ", " + result[2])
                    i = i + 1
            else:
                print("No results found!")
                continue
            while (1):
                print("Enter an index assigned to an artist from selection to see details on songs they performed. Enter q to exit.")
                artistID = input()
                if artistID == '':
                    print("Please give an input.")
                    continue
                elif artistID == 'q':
                    print("Exiting.")
                    break
                elif int(artistID) > len(results) -1:
                    print("Given index is out of range. Try again")
                    continue
                foundArtist = 0
                for i in range(len(results)+1):
                    if artistID == str(i):
                        foundArtist = foundArtist + 1
                        print("Songs:")
                        getResult = getSongs(results[i][0][6:])
                        while(1):
                            for result in getResult:
                                print(result[0] + ", " + result[1] + ", " + result[2])
                            print("Select a song to start performing actions (Give sid). Enter 'q' to quit.")

                            songSelected = input()

                            if songSelected == "":
                                print("Please give an input.")
                                continue
                            elif songSelected == 'q':
                                print("Exiting:")
                                break
                            foundSong = 0
                            for resultSong in getResult:
                                if songSelected == resultSong[0][9:]:
                                    foundSong = foundSong + 1
                                    sno = songActions(uid, sno, songSelected)
                                    break
                            if foundSong == 0:
                                print("Song not found. Please enter a proper ID within the list of songs returned.")
                            continue
                if foundArtist == 0:
                    print("Artist not found. Please enter an index assigned to an artist within the list of artists returned.")
                    continue
            
        elif (x == '4'):
            if (sno is None):
                print("You don't have a session !")
                continue
            else:
                endSession(uid, sno)
                sno = None
        elif (x == '2'):
            print("Enter space separated keywords you'd like to search by ! (e.g 'Fun Songs')")
            keywords = input()
            if keywords == '':
                print("Enter an input properly !")
                continue
            results = spSearch(keywords)
            if len(results) > 5:
                for i in range(5):
                    print(results[i][0] + ", " + results[i][1] + ", " + results[i][2]) #if you want the # of matches, use [3]
                print("There are more than 5 matches ! Do you want to see the rest ? ! ?")
                y = input('Y or N: ')
                if (y.upper() == 'Y'):
                    print('Showing all results ! :')
                    for result in results:
                        print(result[0] + ", " + result[1] + ", " + result[2])
                elif (y.upper() == 'N'):
                    print('Oh well whatever !')
                else:
                    print("Y or N bozo ! You don't get to see the rest then !")
                    # could maybe have this loop. i say just leave it
            else:
                for result in results:
                    print(result[0] + ", " + result[1] + ", " + result[2])
            print("")

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
    
def findArtist(keywords):
    global connection, cursor

    wordSpaced = (keywords.lower()).split()
    words = ['%' + w + '%' for w in wordSpaced]

    nameQuery1 = "SELECT 'Name: ' || artists.name, 'Nationality: ' || artists.nationality, 'Total song(s) performed: ' || count(perform.sid), "
    nameQuery2 =  " FROM artists, perform WHERE artists.aid = perform.aid group by artists.name having allWords > 0 order by allWords desc;"
    
    for thisWord in words:
        nameQuery1 = nameQuery1 + "(artists.name like ?)"
        if thisWord is not words[-1]:
            nameQuery1 += '+'

        
    nameQuery1 += ' as allWords' + nameQuery2
        

    cursor.execute(nameQuery1, words)
    results1 = cursor.fetchall()

    songQuery1 = """
    SELECT 'Name: ' || artists.name, 'Nationality: ' || artists.nationality, 'Total song(s) performed: ' || count(perform.sid), """

    songQuery2 = """
    
    FROM artists, perform, songs 
    WHERE artists.aid = perform.aid and perform.sid = songs.sid
    GROUP BY artists.name
    HAVING allWords > 0
    ORDER BY allWords DESC;
    """
    for thisWord in words:
        songQuery1 += "(songs.title LIKE ?)"
        if thisWord is not words[-1]:
            songQuery1+= '+'

    songQuery1 +='AS allWords' + songQuery2

    cursor.execute(songQuery1, words)
    results2 = cursor.fetchall()
    
    results = results1 + results2


    results.sort(key=lambda tup: tup[3], reverse=True)
    return results

def getSongs(name):
    global connection, cursor
    cursor.execute('SELECT "Song ID: " || songs.sid, "Title: " || songs.title, "Song Duration: " || songs.duration from songs, perform, artists where songs.sid = perform.sid and perform.aid = artists.aid and artists.name like upper(?)', (name,))
    result = cursor.fetchall()
    return result

def getSongsPlaylist(pid):
    global connection, cursor
    cursor.execute('SELECT "Song ID: " || songs.sid, "Title: " || songs.title, "Song Duration: " || songs.duration from songs, plinclude where songs.sid = plinclude.sid and plinclude.pid like ?', (pid,))
    result = cursor.fetchall()
    return result


def songActions(uid, sno, sid):
    global connection, cursor
    while(1):

        cursor.execute('SELECT songs.title FROM songs WHERE songs.sid = ?', (sid,))
        songTitle = cursor.fetchone()
        print("You selected the song: " + songTitle[0] + "! What do you wanna do? Press 1 to listen, 2 to see more info, 3 to add it to a playlist, and q to exit.")

        choice = input()

        if(choice == '1'):
            # listening to song
            print("Starting listening event.")
            if (sno == None):
                sno = addSession(uid)

            cursor.execute('SELECT * FROM listen WHERE uid=? and sno = ? and sid = ?', ((uid, sno, sid)))
            listenExists = cursor.fetchone()
            if (listenExists is not None):
                print("Listening event exists. Adding to event.")
                cursor.execute('UPDATE listen SET cnt = cnt + 1 WHERE uid = ? AND sno = ? AND sid = ?;', (uid, sno, sid))
                connection.commit()
            else:
                print("Listening event does not exists. Creating new listen event.")
                cursor.execute('INSERT INTO listen values (?, ?, ?, ?);', (uid, sno, sid, 1))
                connection.commit()

            print("You have finished listening. Man was that song was awful.")
            continue

        elif (choice == '2'):
            # View more info

            print('Displaying info of the song:')

            query1 = "SELECT 'Artist name: ' || artists.name from artists, perform where artists.aid = perform.aid and perform.sid = ?"

            query2 = "SELECT 'Song ID: ' || songs.sid, 'Title: ' || songs.title, 'Song Duration: ' || songs.duration from songs where songs.sid = ?"

            query3 = "SELECT 'Playlists: ' || playlists.title from playlists, plinclude where playlists.pid = plinclude.pid and plinclude.sid = ?"


            print('Artist(s) who performed the song:')


            cursor.execute(query1, (sid,))

            results = cursor.fetchall()

            for result in results:
                print(result[0])

            print('Song details:')

            cursor.execute(query2, (sid,))

            results = cursor.fetchall()

            for result in results:
                print(result[0] + ', ' + result[1] + ', ' + result[2])


            print('Playlists song is in:')

            cursor.execute(query3,  (sid,))

            
            results = cursor.fetchall()
            inPlaylist = 0
            for result in results:
                inPlaylist = inPlaylist + 1
                print(result[0])

            if inPlaylist == 0:
                print("Currently not in any playlists.")


            print("Done displaying song info.")
            continue


        elif (choice == '3'):
            # Add to the playlist

            # Find if user has playlists:
            print("Displaying Playlists that you created: ")
            cursor.execute('SELECT "Playlist ID: " || playlists.pid, "Playlist Title: " || playlists.title from playlists, users WHERE playlists.uid = users.uid AND users.uid like ?', (uid,))
            getPlaylist = cursor.fetchall()
            hasPlaylist = 0
            for playlist in getPlaylist:
                print(playlist[0] + ", " + playlist[1])
                hasPlaylist= hasPlaylist + 1
            if hasPlaylist == 0:
                print("You currently have no playlists!")
            print("Select a playlist you want to enter the song in (give the PID), or if you want to create a new playlist, enter 'new':")
            while(1):
                selectPid = input()
                if selectPid == '':
                    print("PLEASE GIVE A PID")
                    continue
                elif selectPid == 'new':
                    print("Please give a title to the playlist:")
                    while(1):
                        getTitle = input()
                        if getTitle == '':
                            print("PLEASE GIVE A TITLE")
                            continue
                        cursor.execute('SELECT MAX(pid+0) FROM playlists')
                        pid = cursor.fetchone()
                        if (pid[0] is None):
                            pid = 1
                        else:
                            pid = pid[0] + 1
                            cursor.execute('INSERT INTO playlists VALUES (?,?,?)', (pid, getTitle, uid))
                            print("Created playlist.")
                            cursor.execute('INSERT INTO plinclude VALUES (?,?,?)', (pid, sid, 1))
                            connection.commit()
                            print("Added song into the playlist.")
                            break

                else:
                    isPlaylist = 0
                    for playlist in getPlaylist:
                        if (selectPid == playlist[0][13:]):
                            isPlaylist = isPlaylist + 1
                            cursor.execute('SELECT * from plinclude where plinclude.pid = ? and plinclude.sid = ?', (selectPid, sid))
                            hasEntry = cursor.fetchone()
                            if (hasEntry is not None):
                                print("This playlist already has the song in it! Select a different playlist, or create a new one!")
                                continue
                            cursor.execute('SELECT MAX(sorder+0) from plinclude where plinclude.pid = ?', (selectPid,))
                            sorder = cursor.fetchone()
                            sorder = sorder[0] + 1
                            cursor.execute('INSERT INTO plinclude VALUES (?,?,?)', (selectPid, sid, sorder))
                            connection.commit()
                            print("Added song into the playlist.")
                            break
                    if isPlaylist == 0:
                        print("GIVEN PID IS NOT IN YOUR PLAYLISTS! ENTER A PROPER PID OR CREATE A NEW PLAYLIST!")
                        continue
                break
            continue


        elif (choice == 'q'):
            print("Exiting:")
            return sno

        else:

            print("INCORRECT INPUT. GIVE VALUES OF EITHER 1, 2, OR 3.")
            continue

    return

def spSearch(input):
    global connection, cursor
    # get space-separated keywords
    temp = (input.lower()).split()
    temp2 = ['%' + t + '%' for t in temp]
    keywords = tuple(temp2)
    query1 = "SELECT 'Song ID: ' || sid, title, 'Duration: ' || duration || ' seconds', "
    final1= " FROM songs GROUP BY sid, title, duration HAVING matches > 0 ORDER BY matches DESC;"
    
    # find matching keywords
    for keyword in keywords:
        query1 += "(title LIKE ?)"
        if keyword is not keywords[-1]:
            query1+= '+'

    query1+=' AS matches' + final1

    cursor.execute(query1, keywords)
    results1 = cursor.fetchall()

    query2 = """
    SELECT 'Playlist ID: ' || p.pid, p.title, 'Total Duration: ' || SUM(s.duration) || ' seconds', """

    final = """
     FROM playlists p, plinclude pl, songs s
    WHERE p.pid = pl.pid
    AND pl.sid = s.sid
    GROUP BY p.pid, p.title
    HAVING matches > 0
    ORDER BY matches DESC;
    """
    for keyword in keywords:
        query2 += "(p.title LIKE ?)"
        if keyword is not keywords[-1]:
            query2+= '+'

    query2+='AS matches' + final

    cursor.execute(query2, keywords)
    results2 = cursor.fetchall()
    
    results = results1 + results2
    results.sort(key=lambda tup: tup[3], reverse=True)
    return results
