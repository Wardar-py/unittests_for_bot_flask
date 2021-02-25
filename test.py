from unittest import TestCase, mock
from unittest.mock import patch
from bot import chat
from datetime import datetime
import requests
import requests_mock
import os

class TestApp(TestCase):

    def test_funtranslate(self):#1

        chat_obj = chat()
        with patch.object(chat_obj, 'get_funtranslate', wraps=chat_obj.get_funtranslate) as wrapped_get_funtranslate:
            chat_obj.response("!!funtranslate" + "a")
            wrapped_get_funtranslate.assert_called_with("a")

    def test_date(self):#2
        chat_obj = chat()
        result = chat_obj.response("!!date")
        self.assertEqual(result, "The date is: " + str(datetime.today()))

    def test_date2(self):#3
        chat_obj = chat()
        result = chat_obj.response("!!date")
        self.assertIsNot(result, "The date is: " + str(datetime.isoweekday(datetime.today())))


    @mock.patch.dict(os.environ, {"covidapikey": "mytemp"})
    def test_date(self):#4
        session = requests.Session()
        adapter = requests_mock.Adapter()
        session.mount('mock://', adapter)
        adapter.register_uri('GET', 'https://api.funtranslations.com/translate/valspeak.json?text=')

        chat_obj = chat()
        result = chat_obj.get_funtranslate("")
        self.assertIsNone(result)


    def test_funtranslate1(self):#5
        chat_obj = chat()
        with patch.object(chat_obj, 'get_funtranslate', wraps=chat_obj.get_funtranslate) as wrapped_get_funtranslate:
            chat_obj.response("!!funtranslate" + "brifing")
            wrapped_get_funtranslate.assert_called_with("brifing")


    def test_help(self):#6
        chat_obj = chat()
        result = chat_obj.response("!!help")
        self.assertNotEqual(result, "The commands i respond to are !! followed by either help,about,date")

    def test_about(self):#7
        chat_obj = chat()
        result = chat_obj.response("!!about")
        self.assertEqual(result, "This a little about me, im a chatbout"
                                 " but also i have a chatroom that communicate with other peopple")

    def test_about2(self):#8
        chat_obj = chat()
        rez = chat_obj.response("!!about")
        self.assertTrue(rez, "This a little about me")

    def test_color(self):#9
        chat_obj = chat()
        rez = chat_obj.response("!!Whats my favorite color")
        self.assertIsNot(rez, "")


    def test_covid(self):#10

        chat_obj = chat()
        rez = chat_obj.response("!!test")
        self.assertEqual(rez, "command not recognized")


