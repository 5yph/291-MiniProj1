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
