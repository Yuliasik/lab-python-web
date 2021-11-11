from datetime import datetime
import os
from sys import version

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required

from . import app, db, bcrypt, App
from .forms import LoginForm, RegistrationForm
from .models import User

operating_system = os.name
local_time = datetime.now().strftime("%H:%M:%S")
is_show_about_me = True
is_show_contacts = False


@app.route('/')
def index():
    return render_template("main.html",
                           menu=App.getMenu(),
                           operating_system_front=operating_system,
                           user_agent_front=request.user_agent,
                           version_front=version,
                           local_time_front=local_time
                           )


@app.route("/about")
def about():
    return render_template("about.html",
                           menu=App.getMenu(),
                           operating_system_front=operating_system,
                           user_agent_front=request.user_agent,
                           version_front=version,
                           local_time_front=local_time,
                           is_show_about_me_front=is_show_about_me
                           )


@app.route("/contacts")
def score():
    return render_template("contacts.html",
                           menu=App.getMenu(),
                           operating_system_front=operating_system,
                           user_agent_front=request.user_agent,
                           version_front=version,
                           local_time_front=local_time
                           )


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already loggined in!', category='warning')
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=bcrypt.generate_password_hash(str(form.password.data)))
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data} registered!', category='success')
        return redirect(url_for('login'))
    return render_template('register.html',
                           form=form,
                           menu=App.getMenu(),
                           operating_system_front=operating_system,
                           user_agent_front=request.user_agent,
                           version_front=version,
                           local_time_front=local_time)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already loggined in!', category='warning')
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user_from_db = User.query.filter_by(email=form.email.data).first()
            email = user_from_db.email
            password = user_from_db.password
        except AttributeError:
            flash('Invalid login or password', category='warning')
            return redirect(url_for('login'))

        if form.email.data == email and user_from_db.verify_password(form.password.data):
            login_user(user_from_db, remember=True)
            flash(f'Logged in by username {user_from_db.username}!', category='success')
            return redirect(url_for('about'))
        else:
            flash('Invalid login or password', category='warning')

    return render_template('login.html',
                           form=form,
                           menu=App.getMenu(),
                           operating_system_front=operating_system,
                           user_agent_front=request.user_agent,
                           version_front=version,
                           local_time_front=local_time)


@app.route("/users")
def users():
    all_users = User.query.all()
    count = User.query.count()

    return render_template('users.html',
                           all_users=all_users,
                           count=count,
                           menu=App.getMenu(),
                           operating_system_front=operating_system,
                           user_agent_front=request.user_agent,
                           version_front=version,
                           local_time_front=local_time)


@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('index'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html',
                           user=current_user, menu=App.getMenu(),
                           operating_system_front=operating_system,
                           user_agent_front=request.user_agent,
                           version_front=version,
                           local_time_front=local_time)
