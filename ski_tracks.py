from resource import Resource
import config
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class SkiTracks(Resource):

    def __init__(self):
        super().__init__(config.ski_tracks_api, 'json')
        self.locations = {
                    'Hiukkavaara-Auranmaja 11km' : 'Hiukkavaara - Auranmaja (11km)',
                    'Auranmaja 1,2,3,5 km' : 'Auranmaja (3/5km)',
                    'Auranmaja-Kuivasranta- Vahtola-Niittyaro 10km' : 'Niittyaro - Auranmaja (10km)',
                    'Herukka-Ahvenoja 4.5km' : 'Herukka-Ahvenoja (4.5km)'
                  }

    def __location_mapping(self, location):
        try:
            return self.locations[location]
        except KeyError:
            logging.error("Location mapping not found: {}".format(e))
            return None

    def maintenance_status(self):
        data = []
        json = self.from_endpoint('operations')
        if json:
            for i in json:
                if i['description'] in self.locations:
                    mapped = self.__location_mapping(i['description'])
                    if mapped:
                        i['description'] = mapped
                    data.append(i)
        else:
            logging.error("Ski tracks maintenance data not found.")
        return data