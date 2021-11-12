import sqlite3
import config

def changeParams(file_path, car_value):
    con = sqlite3.connect(config.db)
    cur = con.cursor()

    cur.execute(f'INSERT INTO config (map, car_value) VALUES ("{file_path}", {car_value})')

    con.commit()
    con.close()

