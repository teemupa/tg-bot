import unittest
from unittest import mock
from ruuvi import Ruuvi
import datetime
import datetime

class TestRuuvi(unittest.TestCase):

    @mock.patch('mysql.connector.connect', autospec=True)
    def test_get_all_query_ok(self, mock_connect):
        ruuvi = Ruuvi()
        conn = mock_connect.return_value
        cursor = conn.cursor.return_value
        cursor.fetchone.return_value = (25.0, 89.9, 899.0, datetime.datetime(2021, 4, 25, 15, 8, 24))
        test_data ={
                    'indoor': {'humidity': 89.9,
                                'pressure': 899.0,
                                'temperature': 25.0,
                                'time': datetime.datetime(2021, 4, 25, 15, 8, 24)},
                    'outdoor': {'humidity': 89.9,
                                'pressure': 899.0,
                                'temperature': 25.0,
                                'time': datetime.datetime(2021, 4, 25, 15, 8, 24)},
                    'sauna': {'humidity': 89.9,
                                'pressure': 899.0,
                                'temperature': 25.0,
                                'time': datetime.datetime(2021, 4, 25, 15, 8, 24)}
                    }

        data = ruuvi.get_all()
        self.assertEqual(data, test_data)


if __name__ == '__main__':
    unittest.main()