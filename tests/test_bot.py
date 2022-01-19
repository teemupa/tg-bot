import unittest
from unittest.mock import Mock
from unittest.mock import patch
import bot
import config
from ruuvi import Ruuvi
import datetime

class TestBot(unittest.TestCase):

    def setUp(self):
        self.m_update = Mock()
        self.m_update.effective_chat.id = 0
        self.m_update.message.from_user = {'id':config.me}
        self.m_context = Mock()
    
    def tearDown(self):
        pass

    @patch.object(Ruuvi, 'get_all')
    def test_ruuvi_query_ok(self, get_all):
        get_all.return_value = {'sauna':{'temperature': 25.0, 'humidity': 89.1, 'pressure': 899.89, 'time': datetime.datetime(2009, 1, 6, 15, 8, 24)}}

        message = ( "<b>Sauna</b>" +
                    "\n\U0001f321 " + str(get_all.return_value['sauna']['temperature']) + "\u00b0C" +
                    "\n\U0001F4A7 " + str(get_all.return_value['sauna']['humidity']) + "%" + 
                    "\n\U0001F4A8 " + str(get_all.return_value['sauna']['pressure']) + "hPa" + 
                    "\n\U0001F550 " + str(get_all.return_value['sauna']['time'])
                   )
        
        bot.ruuvi(self.m_update, self.m_context)
        
        #Check sent message.
        self.m_context.bot.send_message.assert_called()
        self.m_context.bot.send_message.assert_called_with(chat_id=0, parse_mode='HTML', text=message)

    @patch.object(Ruuvi, 'get_all')
    def test_ruuvi_query_fail(self, get_all):
        get_all.return_value = {}

        bot.ruuvi(self.m_update, self.m_context)
        
        #Check that message wasn't sent.
        self.m_context.bot.send_message.assert_not_called()


if __name__ == '__main__':
    unittest.main()