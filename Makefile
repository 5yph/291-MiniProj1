make:
	python3 projcloud.py p1.db

remove:
	rm p1.db

database:
	sqlite3 p1.db <p1-tables.sql
	sqlite3 p1.db < p1-data.sql

test:
	rm output.txt
	sqlite3 p1.db <p1-queries.sql >output.txt