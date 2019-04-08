from flask import Flask, render_template, redirect, url_for, g, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from passlib.hash import sha256_crypt
import hashlib
import random
import requests
import json
import datetime

import forms
import models

DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

app = Flask(__name__)
app.secret_key = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(username):
    try:
        return models.User.get(models.User.username == username)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/', methods=('GET', 'POST'))
def home_screen():
    form = forms.Login()
    return render_template('login.html', form=form)


@app.route('/', methods=('GET', 'POST'))
def register():
    form = forms.Login()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Authentication Error", "Error")
        else:
            if sha256_crypt.verify(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
                login_user(user)
                flash("You're Logged in!", "Success")
                return redirect(url_for('index'))
            else:
                flash("Authentication Error", "Error")
    else:
        return render_template('login.html', form=form)


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
