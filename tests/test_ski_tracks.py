import unittest as ut
from unittest import mock
from ski_tracks import SkiTracks

class TestSkiTracks(ut.TestCase):

    @mock.patch('requests.get', autospec=True)
    def test_ski_tracks_ok(self, mock_response):
        tracks = SkiTracks()
        mock_response.return_value.status_code = 200
        test_json = [
            {'maintainedAt':'2022-03-28T13:20:47Z','description':'Hiukkavaara-Auranmaja 11km'},
            {'maintainedAt':'2022-03-28T13:20:47Z','description':'Auranmaja 1,2,3,5 km'}
        ]
        mock_response.return_value.json.return_value = test_json

        expected_status = [
            ('Hiukkavaara - Auranmaja (11km)', '28.03.2022 @ 16:20'),
            ('Auranmaja (3/5km)', '28.03.2022 @ 16:20')
            ]

        status = tracks.maintenance_status()

        self.assertEqual(expected_status, status)

    @mock.patch('requests.get', autospec=True)
    def test_ski_tracks_ok(self, mock_response):
        tracks = SkiTracks()
        mock_response.return_value.status_code = 200
        test_json = [
            {'maintainedAt':'2022-03-28T13:20:47Z','InvalidKey':'Hiukkavaara-Auranmaja 11km'},
        ]
        mock_response.return_value.json.return_value = test_json

        expected_status = []

        status = tracks.maintenance_status()

        self.assertEqual(expected_status, status)

    @mock.patch('requests.get', autospec=True)
    def test_ski_tracks_empty(self, mock_response):
        tracks = SkiTracks()
        mock_response.return_value.status_code = 404
        test_json = []
        mock_response.return_value.json.return_value = test_json

        expected_status = []

        status = tracks.maintenance_status()

        self.assertEqual(expected_status, status)

if __name__ == '__main__':
    ut.main()