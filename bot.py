import time
import json
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime
import os
import flask
import flask_sqlalchemy
import flask_socketio
import time


class chat:

    def get_funtranslate(self, input):

        headers = {'Content-Type': 'application/json'}
        api_url = 'https://api.funtranslations.com/translate/valspeak.json?text=' + input

        response = requests.get(api_url, headers=headers)
        print(response)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return None


#---------------------------------------------------------------------------------------------------------------------------------------------

    def get_covid_info(self):
        dotenv_path = join(dirname(__file__), 'sql.env')
        load_dotenv(dotenv_path)
        url = "https://rapidapi.p.rapidapi.com/v1/total"
        Covidapikey= os.environ['covidapikey']

        querystring = {"country":"USA"}

        headers = {
            'Content-Type': 'application/json',
            'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com",
            'x-rapidapi-key': Covidapikey
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text)

        return "Recovered in USA: " + str(json.loads(response.text)['data']['recovered'])

#---------------------------------------------------------------------------------------------------------------------------------------------




    def response(self, input):
        if(input == "!!about"):
            return "This a little about me, im a chatbout but also i have a chatroom that communicate with other peopple"
        elif(input == "!!help"):
            return "The commands i respond to are !! followed by either help,about,date, Whats my favorite color, covid, or funtranslate (your message here)"
        elif(input == "!!date"):
            return "The date is: " + str(datetime.today())
        elif(input == "!!Whats my favorite color"):
            return "BLue"
        elif (input == "!!covid"):
            return self.get_covid_info()
        elif (input.startswith("!!funtranslate")):
            return self.get_funtranslate(input[14:])['contents']['translated']
        else:
            return "command not recognized"
