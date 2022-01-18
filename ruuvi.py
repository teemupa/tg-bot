#!/usr/bin/env python3

import mysql.connector
import config

class Ruuvi:
    def __init__(self):
        self.mydb = mysql.connector.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.database
        )

    def get_all(self):
        #TODO exception handling
        locations = ['sauna', 'indoor', 'outdoor']
        mycursor = self.mydb.cursor()
        data = {}
        for i in locations:
            spell = "SELECT temperature, humidity, pressure, time FROM ruuvi_measurements WHERE location = %s ORDER BY id DESC LIMIT 1"
            location = (i, )
            mycursor.execute(spell, location)
            myresult = mycursor.fetchone()
            data.update({i : {
                                'temperature' : myresult[0],
                                'humidity' : myresult[1], 
                                'pressure' : myresult[2], 
                                'time' : myresult[3]
                              }
                        })
        return data