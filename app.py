import requests, json, datetime
from flask import Flask, render_template
import hashlib
import random

import forms

DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

app = Flask(__name__)
app.secret_key = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()


@app.route('/', methods=('GET', 'POST'))
def home_screen():
    form = forms.Login()
    return render_template('login.html', form=form)


@app.route('/', methods=('GET', 'POST'))
def register():
    form = forms.Login()
    return render_template('register', form=form)


@app.route('/aq')
def air_quality():
    url = "https://aaws.louisvilleky.gov/api/v1/Monitor/CityAQI"
    res = requests.get(url)
    data = json.loads(res.text)
    curr_time = datetime.datetime.now().strftime("%A, %d %B %Y (%H:%M)")
    site_list = []
    for site in data['Sites']:
        site_name = site['SiteDescription']
        if site['Readings'] is not None:
            readings = site['Readings']
            readings_list = []
            for reading in readings:
                reading_text = reading['ParameterDescription'] + ": " + str(reading['Average']) + " " + reading['Units']
                readings_list.append(reading_text)
        site_list.append([site_name, readings_list])
    return render_template('aq_data.html', site_list=site_list, curr_time=curr_time)


if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT, host=HOST)
