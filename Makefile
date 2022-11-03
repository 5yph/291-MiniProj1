make:
	python3 projcloud.py test.db

remove:
	rm test.db

database:
	sqlite3 test.db < p1-tables.sql
	sqlite3 test.db < p1-data.sql

test:
	rm output.txt
	sqlite3 test.db <p1-queries.sql >output.txt