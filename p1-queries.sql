.echo on

----- Test songs
SELECT *
FROM songs;
-----

-- Test perform
SELECT *
FROM perform;
--

-- -- Test sessions
-- SELECT *
-- FROM sessions
-- WHERE sessions.uid = "u1";
-- -- 

-- get song shit
SELECT *
FROM songs, perform, artists
WHERE perform.aid = artists.aid
AND perform.sid = songs.sid
AND artists.aid='a1';


-- THIS GETS THE USERS WHO LISTENED TO
-- ARTISTS A1 THE MOST IN TERMS OF CNT*DURATION
select l.uid, p.aid, sum(l.cnt*s.duration) as q
from listen l, songs s, perform p
where l.sid=s.sid and s.sid=p.sid and p.aid = 'a1'
group by l.uid
order by q desc;
--limit 3;

-- Get number of playlist each song is in
-- SELECT songs.sid, playlists.pid, COUNT(playlists.pid)
-- FROM songs
-- LEFT OUTER JOIN plinclude 
-- ON songs.sid = plinclude.sid
-- LEFT OUTER JOIN playlists
-- ON playlists.pid = plinclude.pid
-- GROUP BY songs.sid;

-- Get number of playlist each song is in (no joins)
-- also only include songs from particular artist
-- since no joins, this doesn't include songs in 0 playlists
SELECT playlists.pid, songs.sid, COUNT(playlists.pid) AS pcnt
FROM songs, plinclude, playlists, perform
WHERE songs.sid = plinclude.sid
AND playlists.pid = plinclude.pid
AND songs.sid = perform.sid
AND perform.aid = 'a1' -- only lady gaga
GROUP BY playlists.pid
ORDER BY pcnt DESC;

-- Same as above but only select relevant stuff
SELECT playlists.pid, playlists.title, COUNT(playlists.pid) AS pcnt
FROM songs, plinclude, playlists, perform
WHERE songs.sid = plinclude.sid
AND playlists.pid = plinclude.pid
AND songs.sid = perform.sid
AND perform.aid = 'a11' -- only pitbull
GROUP BY playlists.pid
ORDER BY pcnt DESC;
