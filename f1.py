from resource import Resource
import config
from datetime import date
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class F1(Resource):

    def __init__(self):
        super().__init__(config.ergast_api, 'json')

    def driver_standings(self):
        standings = self.from_endpoint(str(date.today().year) + '/driverStandings.json' )
        return None

    def constructor_standings(self):
        standings = self.from_endpoint(str(date.today().year) + '/constructorStandings.json' )
        return None