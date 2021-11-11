from datetime import datetime
import os
from sys import version

from flask import render_template, request

from . import app, App

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
