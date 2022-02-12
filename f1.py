from resource import Resource
import config
from datetime import date
import logging
from datetime import datetime, timezone

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class F1(Resource):

    def __init__(self):
        super().__init__(config.ergast_api, 'json')

    def driver_standings(self):
        standings_list = []
        response = self.from_endpoint(str(date.today().year) + '/driverStandings.json' )
        if response:
            try:
                standings = response['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
                for i in standings:
                    standings_list.append((i['position'], i['points'], i['Driver']['familyName']))
            except (KeyError, IndexError) as e:
                logging.error("Error: {}".format(e))
        return standings_list

    def constructor_standings(self):
        standings_list = []
        response = self.from_endpoint(str(date.today().year) + '/constructorStandings.json' )
        if response:
            try:
                standings = response['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
                for i in standings:
                    standings_list.append((i['position'], i['points'], i['Constructor']['name']))
            except (KeyError, IndexError) as e:
                logging.error("Error: {}".format(e))

        return standings_list

    def season(self):
        season_list = []
        response = self.from_endpoint(str(date.today().year) + '.json')
        if response:
            try:
                season = response['MRData']['RaceTable']['Races']
                for i in season:
                    #Change the date format
                    racedate = datetime.strptime(i['date'], '%Y-%m-%d')
                    racedate = racedate.replace(tzinfo=timezone.utc).astimezone(tz=None)
                    i['date'] = racedate.strftime('%d.%m.%Y')
                    season_list.append((i['date'], i['raceName']))
            except KeyError as e:
                logging.error("KeyError: {}".format(e))

        return season_list