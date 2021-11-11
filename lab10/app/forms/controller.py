from datetime import datetime
import os
from sys import version

from flask import render_template, request, session, flash

from .. import App

from .forms import Form
from .file_writer import FileWriter
from .validation import validate

from . import form

operating_system = os.name
local_time = datetime.now().strftime("%H:%M:%S")
is_show_about_me = True
is_show_contacts = False


@form.route('/form', methods=['GET', 'POST'])
def form():
    form = Form()
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
