import unittest as ut
from unittest import mock
import bot
import config
import datetime
from ruuvi import Ruuvi
from ski_tracks import SkiTracks

class TestBot(ut.TestCase):

    def setUp(self):
        self.m_update = ut.mock.Mock()
        self.m_update.effective_chat.id = 0
        self.m_update.message.from_user = {'id':config.users[0]}
        self.m_context = ut.mock.Mock()

    @mock.patch.object(Ruuvi, 'get_all')
    def test_ruuvi_query_ok(self, get_all):
        get_all.return_value = {'sauna':{'temperature': 25.0, 'humidity': 89.1, 'pressure': 899.89, 'time': datetime.datetime(2021, 4, 25, 15, 8, 24)}}

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

    @mock.patch.object(Ruuvi, 'get_all')
    def test_ruuvi_query_fail(self, get_all):
        get_all.return_value = {}

        bot.ruuvi(self.m_update, self.m_context)
        
        #Check that message wasn't sent.
        self.m_context.bot.send_message.assert_called()
        self.m_context.bot.send_message.assert_called_with(chat_id=0, parse_mode='HTML', text="ERROR: Ruuvi query failed!")

    @mock.patch.object(SkiTracks, 'maintenance_status')
    def test_ski_tracks_maintentance_status_ok(self, maintenance_status):
        maintenance_status.return_value = [{'description': 'Auranmaja 1,2,3,5 km', 'name': 'Oulu', 'maintainedAt': '28.01.2022 10:43',
                                            'id': 89739149, 'type': 'skitrack'},                                                                                                                                                                                                                                                                                                        
                                            {'description': 'Hiukkavaara-Auranmaja 11km', 'name': 'Oulu', 'maintainedAt': '27.01.2022 22:08',
                                            'id': 89661884, 'type': 'skitrack'},                                                                                                                                                                                                                                                                                                  
                                            {'description': 'Auranmaja-Kuivasranta- Vahtola-Niittyaro 10km', 'name': 'Oulu', 'maintainedAt': '27.01.2022 13:46',
                                            'id': 89618897, 'type': 'skitrack'},                                                                                                                                                                                                                                                                               
                                            {'description': 'Herukka-Ahvenoja 4.5km', 'name': 'Oulu', 'maintainedAt': '27.01.2022 13:07',
                                            'id': 89614764, 'type': 'skitrack'}]

        message = "\n 🎿 <b>Auranmaja 1,2,3,5 km:</b> \n28.01.2022 10:43\n\n "\
                    "🎿 <b>Hiukkavaara-Auranmaja 11km:</b> \n27.01.2022 22:08\n\n "\
                    "🎿 <b>Auranmaja-Kuivasranta- Vahtola-Niittyaro 10km:</b> \n27.01.2022 13:46\n\n "\
                    "🎿 <b>Herukka-Ahvenoja 4.5km:</b> \n27.01.2022 13:07\n"
        
        bot.latu(self.m_update, self.m_context)
        
        #Check sent message.
        self.m_context.bot.send_message.assert_called()
        self.m_context.bot.send_message.assert_called_with(chat_id=0, parse_mode='HTML', text=message)

    @mock.patch.object(SkiTracks, 'maintenance_status')
    def test_ski_tracks_maintentance_status_fail(self, maintenance_status):
        maintenance_status.return_value = []

        bot.latu(self.m_update, self.m_context)
        
        #Check sent message.
        self.m_context.bot.send_message.assert_called()
        self.m_context.bot.send_message.assert_called_with(chat_id=0, parse_mode='HTML', text="ERROR: Maintenance status not found!")

if __name__ == '__main__':
    ut.main()