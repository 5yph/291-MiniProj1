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

def spSearch(input):
    global connection, cursor
    temp = (input.lower()).split()
    temp2 = ['%' + t + '%' for t in temp]
    keywords = tuple(temp2)
    query1 = "SELECT 'Song ID: ' || sid, title, 'Duration: ' || duration || ' seconds', "
    final1= " FROM songs GROUP BY sid, title, duration HAVING matches > 0 ORDER BY matches DESC;"
    
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