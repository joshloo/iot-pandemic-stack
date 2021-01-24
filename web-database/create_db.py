#!/usr/bin/env python

import sqlite3 as lite
import sys
import random

con = lite.connect('covid.db')

with con:
    
    cur = con.cursor() 
    cur.execute("DROP TABLE IF EXISTS user")
    cur.execute("CREATE TABLE user(timestamp DATETIME, username TEXT, \'IC\' TEXT, location TEXT, temperature TEXT)")

    for x in range(100):
        command = "INSERT INTO user VALUES(datetime('now'), 'Loo Tung Lun', '010101-02-0303'," + '\'' \
        + 'lat:' + str(random.randint(1,999)) + '.' + str(random.randint(1,999)) + ',' \
        + 'long:' + str(random.randint(1,999)) + '.' + str(random.randint(1,999)) + '\'' + ',' +'\'' \
        + str(random.randint(35,39)) + '.' + str(random.randint(0,99)) + '\'' + ')'
        print(command)
        cur.execute(command)

con.close()