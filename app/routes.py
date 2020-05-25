from flask import flash, render_template, redirect, url_for

from app import app
from app.forms import LoginForm, Search_params


@app.route('/')
@app.route('/index')
def index():
    title = 'Welcome'
    header = 'Узнайте, что происходит вокруг вас.'
    return render_template('index.html', title=title, header=header)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/location_input', methods=['GET', 'POST'])
def location_input():
    title = 'Fill the form'
    form = Search_params()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('location_input.html', title=title, form=form)
