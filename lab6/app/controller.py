from datetime import datetime
import os
from sys import version

from flask import render_template, request, session, flash

from app import App

from app.forms import LoginForm
from app.file_writer import FileWriter
from app.validation import validate
from app import app

operating_system = os.name
local_time = datetime.now().strftime("%H:%M:%S")
is_show_about_me = True
is_show_contacts = False


@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()
    validate(form)

    if form.validate_on_submit():
        FileWriter().write_to_file(form)
        flash('The user has been written to data.json file')
        session['login'] = form.login.data
        session['e_number'] = form.e_number.data
        return render_template("result.html",
                               form=form,
                               menu=App.getMenu(),
                               operating_system_front=operating_system,
                               user_agent_front=request.user_agent,
                               version_front=version,
                               local_time_front=local_time
                               )
    else:
        session['login'] = ''
        session['e_number'] = ''

    return render_template("form.html",
                           form=form,
                           e_number=session['e_number'],
                           login=session['login'],
                           menu=App.getMenu(),
                           operating_system_front=operating_system,
                           user_agent_front=request.user_agent,
                           version_front=version,
                           local_time_front=local_time
                           )


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
