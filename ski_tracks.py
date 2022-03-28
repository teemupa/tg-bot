from resource import Resource
import config
import logging
from datetime import datetime, timezone

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class SkiTracks(Resource):

    def __init__(self):
        super().__init__(config.ski_tracks_api, 'json')
        self.__locations = {
                    'Hiukkavaara-Auranmaja 11km' : 'Hiukkavaara - Auranmaja (11km)',
                    'Auranmaja 1,2,3,5 km' : 'Auranmaja (3/5km)',
                    'Auranmaja-Kuivasranta- Vahtola-Niittyaro 10km' : 'Niittyaro - Auranmaja (10km)',
                    'Herukka-Ahvenoja 4.5km' : 'Herukka - Ahvenoja (4.5km)'
                  }

    def __location_mapping(self, location):
        try:
            return self.__locations[location]
        except KeyError:
            logging.error("Location mapping not found: {}".format(e))
            return None

    def maintenance_status(self):
        status_list = []
        status = self.from_endpoint('operation/list')
        if status:
            for i in status:
                #Change venue names.
                try:
                    if i['description'] in self.__locations:
                        mapped = self.__location_mapping(i['description'])
                        if mapped:
                            i['description'] = mapped
                            #Adjust timezone and timestamp format.
                            timestamp = datetime.strptime(i['maintainedAt'], '%Y-%m-%dT%H:%M:%S%z')
                            timestamp = timestamp.replace(tzinfo=timezone.utc).astimezone(tz=None)
                            i['maintainedAt'] = timestamp.strftime('%d.%m.%Y @ %H:%M')
                            status_list.append((i['description'], i['maintainedAt']))
                except KeyError as e:
                    logging.error("KeyError: {}".format(e))

        else:
            logging.error("Ski tracks maintenance status_list not found.")

        return status_list
