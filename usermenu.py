import sqlite3
import this
import time

def userMenu(uid, con, cur):
    global connection, cursor, songCursor

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


        elif (x == '3'):
            print('Provide a keyword for artist name, or song they performed, seperated by space:')
            keywords = input()
            results = findArtist(keywords)
            if keywords == '':
                print("Please give an input.")
                continue
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

            else:
                for result in results:
                    print(result[0] + ", " + result[1] + ", " + result[2])

            
            print("Enter an artist's name from selection to see details on songs they performed")
            artistName = input()
            if artistName == '':
                print("Please give an input.")
                continue
            foundArtist = 0
            artistNameCap = artistName.lower()
            for result in results:
                thisRes = result[0][6:].lower() 
                if artistName == thisRes:
                    foundArtist = foundArtist + 1
                    print("Songs:")
                    getResult = getSongs(artistName)
                    for result in getResult:
                        print(result[0] + ", " + result[1] + ", " + result[2])
                    print("Select a song to start performing actions (Give sid): ")

                    songSelected = input()

                    if songSelected == "":
                        print("Please give an input.")
                        continue
                    foundSong = 0
                    for resultSong in getResult:
                        if songSelected == resultSong[0][9:]:
                            foundSong = foundSong + 1
                            songActions(uid, sno, songSelected)

                    
                    if foundSong == 0:
                        print("Song not found. Please enter a proper ID within the list of artists returned.")
                    break
            if foundArtist == 0:
                print("Artist not found. Please enter a name within the list of artists returned.")
            

            


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


def songActions(uid, sno, sid):
    global connection, cursor
    while(1):
        print("Hey, loser! You selected this song! What do you wanna do? Press 1 to listen, 2 to see more info, and 3 to add it to a playlist.")

        choice = input()

        if(choice == 1):
            # listening to song
            print("Starting listening event.")
            if (sno == None):
                sno = addSession(uid)

            cursor.execute('SELECT * FROM listen WHERE uid=? and sno = ? and sid = ?', ((uid, sno, sid)))
            listenExists = cursor.fetchone()
            if (listenExists[0] is not None):
                cursor.execute('UPDATE listen SET cnt = cnt + 1 WHERE uid = ? AND sno = ? AND sid = ?;', (uid, sno, sid))
            else:
                cursor.execute('INSERT INTO listen values (?, ?, ?, ?);', (uid, sno, sid, 1))

            print("You have finished listening. Man was that song was awful.")
            continue

        elif (choice == 2):
            # View more info

            print('Displaying info of the song:')

            query1 = "SELECT artists.name from artists, perform where artists.aid = perform.aid and perform.sid = ?"

            query2 = "SELECT songs.sid, songs.title, songs.duration, from artists, songs, perform where songs.sid = ?"

            query3 = "SELECT playlists.title from playlists, plinclude where playlists.pid = plinclude.pid and plinclude.sid = ?"


            print('Artist(s) who performed the song:')

            cursor.execute(query1, sid)

            results = cursor.fetchall()

            for result in results:
                print(result)

            print('Song details:')

            cursor.execute(query2, sid)

            results = cursor.fetchall()

            for result in results:
                print(result)


            print('Playlists song is in:')

            cursor.execute(query3, sid)

            results = cursor.fetchall()

            for result in results:
                print(result)


            print("Done displaying song info. Cringe.")
            continue


        elif (choice == 3):
            # Add to the playlist

            print("Adding song to playlist:")

            # Find if user has playlists:

            

            # If creating new playlist, select unique pid

            print("Create a name for the playlist:")

            playlistTitle = input()

            cursor.execute('SELECT MAX(pid+0) FROM playlists')
            pid = cursor.fetchone()
            if (pid[0] is None):
                pid = 1
            else:
                pid = pid[0] + 1
            cursor.execute('INSERT INTO playlist VALUES (?,?,?)', (pid, playlistTitle, uid))
            connection.commit()
            return sno

        

        else:

            print("INCORRECT INPUT. GIVE VALUES OF EITHER 1, 2, OR 3.")
            continue




        #  Song actions: When a song is selected, the user can perform any of these actions: (1) listen to it, (2) see more information about it, or (3) add it to a playlist. 
        # More information for a song is the names of artists who performed it in addition to id, title and duration of the song as well as the names of playlists the song is in (if any). 
        # When a song is selected for listening, a listening event is recorded within the current session of the user (if a session has already started for the user) or within a new session (if not). 
        # When starting a new session, follow the steps given for starting a session. A listening event is recorded by either inserting a row to table listen or increasing the listen count in this table by 1. 
        # When adding a song to a playlist, the song can be added to an existing playlist owned by the user (if any) or to a new playlist. When it is added to a new playlist, a new playlist should be created with 
        # a unique id (created by your system) and the uid set to the id of the user and a title should be obtained from input. 

# Artists should be able to perform the following actions:

# Add a song. The artists should be able to add a song by providing a title and a duration. The system should check if the artists already has a song with the same title and duration. If not, the song should be 
# added with a unique id (assigned by your system) and any additional artist who may have performed the song with their ids obtained from input.
# Find top fans and playlists. The artist should be able to list top 3 users who listen to their songs the longest time and top 3 playlists that include the largest number of their songs. If there are less than 
# 3 such users or playlists, fewer number of users and playlists can be returned. 
