import unittest
from unittest.mock import Mock
from unittest.mock import patch
import bot
import config
from ruuvi import Ruuvi
import datetime

class TestBot(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    @patch.object(Ruuvi, "get_all")
    def test_ruuvi(self, get_all):
        m_update = Mock()
        m_update.effective_chat.id = 0
        m_update.message.from_user = {'id':config.me}

        m_context = Mock()

        get_all.return_value = {'sauna':{'temperature': 25.0, 'humidity': 89.1, 'pressure': 899.89, 'time': datetime.datetime(2009, 1, 6, 15, 8, 24)}}

        message = ( "<b>Sauna</b>" +
                    "\n\U0001f321 " + str(get_all.return_value['sauna']['temperature']) + "\u00b0C" +
                    "\n\U0001F4A7 " + str(get_all.return_value['sauna']['humidity']) + "%" + 
                    "\n\U0001F4A8 " + str(get_all.return_value['sauna']['pressure']) + "hPa" + 
                    "\n\U0001F550 " + str(get_all.return_value['sauna']['time'])
                   )
        
        bot.ruuvi(m_update, m_context)
        
        #Check send_message.
        m_context.bot.send_message.assert_called()
        m_context.bot.send_message.assert_called_with(chat_id=0, parse_mode='HTML', text=message)

if __name__ == '__main__':
    unittest.main()