.echo on

----- Test songs
SELECT songs.title
FROM songs;
-----

-- Test sessions
SELECT *
FROM sessions
WHERE sessions.uid = "u1";