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

year = datetime.datetime.now().strftime("%Y")


@login_manager.user_loader
def load_user(username):
    try:
        return models.User.get(username) #(models.User.username == username)
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
def login():
    form = forms.Login()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("Authentication Error", "Error")
        else:
            if sha256_crypt.verify(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
                login_user(user)
                flash("You're Logged in " + user.username + "!", "Success")
                return redirect('/landing')
            else:
                flash("Authentication Error", "Error")
    else:
        return render_template('login.html', form=form, year=year)


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.Register()
    if form.validate_on_submit():
        flash("Yay! you registered!", "success")
        models.User.create_user(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index.html'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/landing')
def landing():
    return render_template('landing.html', year=year)


@app.route('/aq')
@login_required
def air_quality():
    url = "https://aaws.louisvilleky.gov/api/v1/Monitor/CityAQI"
    res = requests.get(url)
    data = json.loads(res.text)
    curr_time = datetime.datetime.now().strftime("%A, %d %B %Y (%H:%M)")
    # year = datetime.datetime.now().strftime("%Y")
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
    return render_template('aq_data.html', site_list=site_list, curr_time=curr_time, year=year)


@app.route('/db_admin_main', methods=('GET', 'POST'))
def db_admin_main():
    return render_template('db_admin_main.html')


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT, host=HOST)
