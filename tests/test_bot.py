import unittest as ut
from unittest import mock
import bot
import config
import datetime
from ruuvi import Ruuvi
from ski_tracks import SkiTracks
from f1 import F1

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
        maintenance_status.return_value = [
            ('Auranmaja 1,2,3,5 km', '28.01.2022 10:43'),
            ('Hiukkavaara-Auranmaja 11km', '27.01.2022 22:08'),
            ('Auranmaja-Kuivasranta- Vahtola-Niittyaro 10km', '27.01.2022 13:46'),
            ('Herukka-Ahvenoja 4.5km', '27.01.2022 13:07')
        ]

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

    @mock.patch.object(F1, 'driver_standings')
    def test_f1_driver_standings_ok(self, driver_standings):
        message = "<b>#\tName\tPoints</b>\n"\
                  "1. Hamilton 40\n"\
                  "2. Vettel 34\n"\
                  "3. Bottas 23"

        self.m_context.args = ['drivers']
        driver_standings.return_value = [
            ('1', '40', 'Hamilton'),
            ('2', '34', 'Vettel'),
            ('3', '23', 'Bottas'),
        ]

        bot.f1(self.m_update, self.m_context)

        self.m_context.bot.send_message.assert_called()
        self.m_context.bot.send_message.assert_called_with(chat_id=0, parse_mode='HTML', text=message)

    @mock.patch.object(F1, 'driver_standings')
    def test_f1_driver_standings_fail(self, driver_standings):
        message = "ERROR: Unable to fetch f1 data!"

        self.m_context.args = ['drivers']
        driver_standings.return_value = []

        bot.f1(self.m_update, self.m_context)

        self.m_context.bot.send_message.assert_called()
        self.m_context.bot.send_message.assert_called_with(chat_id=0, parse_mode='HTML', text=message)

    @mock.patch.object(F1, 'constructor_standings')
    def test_f1_constructor_standings_ok(self, constructor_standings):
        message = "<b>#\tTeam\tPoints</b>\n"\
                  "1. Mercedes 40\n"\
                  "2. Aston Martin 34\n"\
                  "3. Alfa Romeo 23"

        self.m_context.args = ['teams']
        constructor_standings.return_value = [
            ('1', '40', 'Mercedes'),
            ('2', '34', 'Aston Martin'),
            ('3', '23', 'Alfa Romeo'),
        ]

        bot.f1(self.m_update, self.m_context)

        self.m_context.bot.send_message.assert_called()
        self.m_context.bot.send_message.assert_called_with(chat_id=0, parse_mode='HTML', text=message)

    @mock.patch.object(F1, 'constructor_standings')
    def test_f1_constructor_standings_fail(self, constructor_standings):
        message = "ERROR: Unable to fetch f1 data!"

        self.m_context.args = ['teams']
        constructor_standings.return_value = []

        bot.f1(self.m_update, self.m_context)

        self.m_context.bot.send_message.assert_called()
        self.m_context.bot.send_message.assert_called_with(chat_id=0, parse_mode='HTML', text=message)

    @mock.patch.object(F1, 'season')
    def test_f1_season_ok(self, season):
        message = "<b>Season calendar</b>\n"\
                  "20.03.2022: Bahrain Grand Prix\n"\
                  "27.03.2022: Saudi Arabian Grand Prix\n"\
                  "10.04.2022: Australian Grand Prix"

        self.m_context.args = ['season']
        season.return_value = [
            ('20.03.2022', 'Bahrain Grand Prix'),
            ('27.03.2022', 'Saudi Arabian Grand Prix'),
            ('10.04.2022', 'Australian Grand Prix')
        ]

        bot.f1(self.m_update, self.m_context)

        self.m_context.bot.send_message.assert_called()
        self.m_context.bot.send_message.assert_called_with(chat_id=0, parse_mode='HTML', text=message)

    @mock.patch.object(F1, 'season')
    def test_f1_season_fail(self, season):
        message = "ERROR: Unable to fetch f1 data!"

        self.m_context.args = ['season']
        season.return_value = []

        bot.f1(self.m_update, self.m_context)

        self.m_context.bot.send_message.assert_called()
        self.m_context.bot.send_message.assert_called_with(chat_id=0, parse_mode='HTML', text=message)

    def test_f1_no_such_argument(self):
        message = "ERROR: No such argument!"

        self.m_context.args = ['invalid']

        bot.f1(self.m_update, self.m_context)

        self.m_context.bot.send_message.assert_called()
        self.m_context.bot.send_message.assert_called_with(chat_id=0, parse_mode='HTML', text=message)


if __name__ == '__main__':
    ut.main()