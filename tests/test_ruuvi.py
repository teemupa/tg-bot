import unittest
import bot
import config
from ruuvi import Ruuvi
import datetime

class TestRuuvi(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    @unittest.mock.patch('mysql.connector.connect', autospec=True)
    def test_get_all_query_ok(self, mock_connect):
        ruuvi = Ruuvi()
        data = ruuvi.get_all()
        #Use sife effect to change mock for every time fetchone is called?
        #https://stackoverflow.com/questions/64443736/how-to-dynamically-mock-the-result-of-a-python-function-inside-a-for-loop

if __name__ == '__main__':
    unittest.main()