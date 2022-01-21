#!/usr/bin/env python3

import mysql.connector
import config

class Ruuvi:
    def __init__(self):
        self.cursor = None
        self.conn = None
        self.host = config.host
        self.user = config.user
        self.password = config.password
        self.database = config.database

    def __enter__(self):
        self.conn = mysql.connector.connect(
                        host = self.host,
                        user = self.user,
                        password = self.password,
                        database = self.database
                    )
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def get_all(self):
        #TODO exception handling
        locations = ['sauna', 'indoor', 'outdoor']
        data = {}
        with self as cur:
            for i in locations:
                spell = "SELECT temperature, humidity, pressure, time FROM ruuvi_measurements WHERE location = %s ORDER BY id DESC LIMIT 1"
                location = (i, )
                cur.execute(spell, location)
                myresult = self.cursor.fetchone()
                data.update({i : {
                                    'temperature' : myresult[0],
                                    'humidity' : myresult[1], 
                                    'pressure' : myresult[2], 
                                    'time' : myresult[3]
                                }
                            })
        return data