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
-- SELECT *
-- FROM songs, perform, artists
-- WHERE perform.aid = artists.aid
-- AND perform.sid = songs.sid;
-- AND artists.aid='a1'
-- AND songs.title='Applause'
-- AND songs.duration=212;