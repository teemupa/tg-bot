import requests
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class Resource:
    
    def __init__(self, api=None, type='json'):
        self.api = api
        self.type = type

    def from_endpoint(self, endpoint):
        r = requests.get(self.api + endpoint)
        body = {}
        logging.info("GET %s from %s%s", r.status_code, self.api, endpoint)
        if r.status_code == 200:
            if self.type == 'json':
                try:
                    body = r.json()
                except requests.exceptions.JSONDecodeError as e:
                    pass
            elif self.type == 'xml':
                pass
        return body