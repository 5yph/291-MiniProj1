.echo on

----- Test songs
SELECT *
FROM songs;
-----

-- Test perform
SELECT *
FROM perform;
--



-- Test playlists

SELECT *
FROM playlists;


-- Test playlist includes

SELECT *
FROm plinclude, songs
WHERE plinclude.sid = songs.sid and plinclude.pid = '36';
-- -- Test sessions
SELECT *
FROM sessions
WHERE sessions.uid = "u0";
-- 

SELECT *
FROM listen
where listen.uid = 'u0';

-- get song shit
-- SELECT *
-- FROM songs, perform, artists
-- WHERE perform.aid = artists.aid
-- AND perform.sid = songs.sid;
-- AND artists.aid='a1'
-- AND songs.title='Applause'
-- AND songs.duration=212;