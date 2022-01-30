import unittest as ut
from unittest import mock
from resource import Resource
import datetime
import requests

class TestResource(ut.TestCase):

    @mock.patch('requests.get', autospec=True)
    def test_from_endpoint_json_ok(self, response):
        resource = Resource('https://api.com/api/', 'json')
        test_json = {'the_way': 'This is the way.'}
        response.return_value.status_code = 200
        response.return_value.json.return_value = test_json
        body = resource.from_endpoint('mandalorian')
        self.assertEqual(body, test_json)

    @mock.patch('requests.get', autospec=True)
    def test_from_endpoint_json_fail(self, response):
        resource = Resource('https://api.com/api/', 'json')
        response.return_value.status_code = 403
        test_json = {}
        body = resource.from_endpoint('mandalorian')
        self.assertEqual(body, test_json)

    @mock.patch('requests.get', autospec=True)
    def test_from_endpoint_xml_ok(self, response):
        #TODO XML content types are not supported at the moment. Placeholder test.
        resource = Resource('https://api.com/api/', 'xml')
        test_xml = {}
        response.return_value.status_code = 200
        body = resource.from_endpoint('mandalorian')
        self.assertEqual(body, test_xml)

if __name__ == '__main__':
    ut.main()