import sqlite3
from  .config import *

def changeParams(file_path, car_value):
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(f'INSERT INTO config (map, car_value) VALUES ("{file_path}", {car_value})')

    con.commit()
    con.close()

