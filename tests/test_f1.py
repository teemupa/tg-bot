import unittest as ut
from unittest import mock
from f1 import F1
from resource import Resource
import datetime
import requests

class TestF1(ut.TestCase):

    @mock.patch('requests.get', autospec=True)
    def test_driver_standings_ok(self, mock_response):
        f1 = F1()
        mock_response.return_value.status_code = 200
        test_json = {'MRData':{'StandingsTable':{'StandingsLists':[{'DriverStandings':[
            {'position':'1', 'points':'13', 'Driver':{'familyName':'Hamilton'}},
            {'position':'2', 'points':'8', 'Driver':{'familyName':'Verstappen'}},
            {'position':'3', 'points':'8', 'Driver':{'familyName':'Bottas'}}
        ]}]}}}
        mock_response.return_value.json.return_value = test_json
        
        expected_standings = [('1', '13', 'Hamilton'), ('2', '8', 'Verstappen'), ('3', '8', 'Bottas')]

        standings = f1.driver_standings()

        self.assertEqual(expected_standings, standings)

    @mock.patch('requests.get', autospec=True)
    def test_driver_standings_empty(self, mock_response):
        f1 = F1()
        mock_response.return_value.status_code = 403
        test_json = {}
        mock_response.return_value.json.return_value = test_json
        
        expected_standings = []

        standings = f1.driver_standings()

        self.assertEqual(expected_standings, standings)

    @mock.patch('requests.get', autospec=True)
    def test_driver_standings_key_error(self, mock_response):
        f1 = F1()
        mock_response.return_value.status_code = 200
        test_json = {'MRData':{'StandingsTable':{'InvalidKey':[{'DriverStandings':[
            {'position':'1', 'points':'13', 'Driver':{'familyName':'Hamilton'}},
            {'position':'2', 'points':'8', 'Driver':{'familyName':'Verstappen'}},
            {'position':'3', 'points':'8', 'Driver':{'familyName':'Bottas'}}
        ]}]}}}
        mock_response.return_value.json.return_value = test_json
        
        expected_standings = []

        standings = f1.driver_standings()

        self.assertEqual(expected_standings, standings)

    @mock.patch('requests.get', autospec=True)
    def test_driver_standings_index_error(self, mock_response):
        f1 = F1()
        mock_response.return_value.status_code = 200
        test_json = {'MRData':{'StandingsTable':{'StandingsLists':[]}}}
        mock_response.return_value.json.return_value = test_json

        expected_standings = []

        standings = f1.constructor_standings()

        self.assertEqual(expected_standings, standings)

    @mock.patch('requests.get', autospec=True)
    def test_constructor_standings_ok(self, mock_response):
        f1 = F1()
        mock_response.return_value.status_code = 200
        test_json = {'MRData':{'StandingsTable':{'StandingsLists':[{'ConstructorStandings':[
            {'position':'1', 'points':'13', 'Constructor':{'name':'Mercedes'}},
            {'position':'2', 'points':'8', 'Constructor':{'name':'Redbull'}},
            {'position':'3', 'points':'8', 'Constructor':{'name':'Alfa Romeo'}}
        ]}]}}}
        mock_response.return_value.json.return_value = test_json

        expected_standings = [('1', '13', 'Mercedes'), ('2', '8', 'Redbull'), ('3', '8', 'Alfa Romeo')]

        standings = f1.constructor_standings()

        self.assertEqual(expected_standings, standings)

    @mock.patch('requests.get', autospec=True)
    def test_constructor_standings_empty(self, mock_response):
        f1 = F1()
        mock_response.return_value.status_code = 404
        test_json = {}
        mock_response.return_value.json.return_value = test_json

        expected_standings = []

        standings = f1.constructor_standings()

        self.assertEqual(expected_standings, standings)

    @mock.patch('requests.get', autospec=True)
    def test_constructor_standings_key_error(self, mock_response):
        f1 = F1()
        mock_response.return_value.status_code = 200
        test_json = {'MRData':{'InvalidKey':{'StandingsLists':[{'ConstructorStandings':[
            {'position':'1', 'points':'13', 'Constructor':{'name':'Mercedes'}},
            {'position':'2', 'points':'8', 'Constructor':{'name':'Redbull'}},
            {'position':'3', 'points':'8', 'Constructor':{'name':'Alfa Romeo'}}
        ]}]}}}
        mock_response.return_value.json.return_value = test_json

        expected_standings = []

        standings = f1.constructor_standings()

        self.assertEqual(expected_standings, standings)

    @mock.patch('requests.get', autospec=True)
    def test_constructor_standings_index_error(self, mock_response):
        f1 = F1()
        mock_response.return_value.status_code = 200
        test_json = {'MRData':{'StandingsTable':{'StandingsLists':[]}}}
        mock_response.return_value.json.return_value = test_json

        expected_standings = []

        standings = f1.constructor_standings()

        self.assertEqual(expected_standings, standings)

    @mock.patch('requests.get', autospec=True)
    def test_season_ok(self, mock_response):
        f1 = F1()
        mock_response.return_value.status_code = 200
        test_json = {'MRData':{'RaceTable':{'Races':[
            {'date':'2022-07-20', 'raceName':'Belgian Grand Prix'},
            {'date':'2022-06-13', 'raceName':'German Grand Prix'}
        ]}}}
        mock_response.return_value.json.return_value = test_json

        expected_standings = [('20.07.2022', 'Belgian Grand Prix'), ('13.06.2022', 'German Grand Prix')]

        standings = f1.season()

        self.assertEqual(expected_standings, standings)

    @mock.patch('requests.get', autospec=True)
    def test_season_key_error(self, mock_response):
        f1 = F1()
        mock_response.return_value.status_code = 200
        test_json = {'MRData':{'InvalidKey':{'Races':[
            {'date':'2022-07-20', 'raceName':'Belgian Grand Prix'},
            {'date':'2022-06-13', 'raceName':'German Grand Prix'}
        ]}}}
        mock_response.return_value.json.return_value = test_json

        expected_standings = []

        standings = f1.season()

        self.assertEqual(expected_standings, standings)

    @mock.patch('requests.get', autospec=True)
    def test_season_empty(self, mock_response):
        f1 = F1()
        mock_response.return_value.status_code = 404
        test_json = {}
        mock_response.return_value.json.return_value = test_json

        expected_standings = []

        standings = f1.season()

        self.assertEqual(expected_standings, standings)

if __name__ == '__main__':
    ut.main()