from datetime import datetime
import os
import secrets
from PIL import Image

from sys import version

from flask import url_for, request, \
    render_template, flash, redirect, current_app
from .. import db, App
from .forms import RegistrationForm, LoginForm, UpdateAccountForm
from .models import User
from flask_login import login_user, current_user, logout_user, login_required

from . import auth

operating_system = os.name
local_time = datetime.now().strftime("%H:%M:%S")
is_show_about_me = True
is_show_contacts = False


@auth.route('/')
def index():
    return redirect(url_for('login'))


@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already loggined in!', category='warning')
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data} registered!', category='success')
        return redirect(url_for('auth.login'))
    return render_template('register.html',
                           form=form,
                           menu=App.getMenu(),
                           operating_system_front=operating_system,
                           user_agent_front=request.user_agent,
                           version_front=version,
                           local_time_front=local_time)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already loggined in!', category='warning')
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user_from_db = User.query.filter_by(email=form.email.data).first()
            email = user_from_db.email
        except AttributeError:
            flash('Invalid login or password', category='warning')
            return redirect(url_for('auth.login'))

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


@auth.route("/users", methods=['GET', 'POST'])
@login_required
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


@auth.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('index'))


@auth.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your accounts data are updated", category="success")
        return redirect(url_for('auth.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image = url_for('static',
                    filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',
                           user=current_user, menu=App.getMenu(),
                           operating_system_front=operating_system,
                           user_agent_front=request.user_agent,
                           version_front=version,
                           local_time_front=local_time,
                           image=image,
                           form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,
                                'static\\profile_pics', picture_filename)
    output_size = (150, 150)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    return picture_filename
