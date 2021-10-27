from datetime import datetime
import os
from sys import version

from flask import render_template, request

from application import Application

from wtforms.validators import InputRequired, Length, Regexp

from forms import LoginForm
from file_writer import FileWriter

app = Application().getApplication()
operating_system = os.name
local_time = datetime.now().strftime("%H:%M:%S")
is_show_about_me = True
is_show_contacts = False


@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()

    if form.e_year.data is not None:
        regex = ''
        length = 0

        if int(form.e_year.data) < 2015:
            regex = '^[A-Z]{2}$'
            length = 8
        else:
            regex = '^[A-Z][0-9]{2}$'
            length = 6

        form.d_series.validators = [Regexp(regex=regex,
                                           message=form._8)]

        form.d_number.validators = [InputRequired(form._3),
                                    Length(min=length,
                                           max=length,
                                           message=form._9)]

    if form.validate_on_submit():
        FileWriter().write_to_file(form)
        return render_template("result.html",
                               form=form,
                               menu=Application.getMenu(),
                               operating_system_front=operating_system,
                               user_agent_front=request.user_agent,
                               version_front=version,
                               local_time_front=local_time
                               )

    return render_template("form.html",
                           form=form,
                           menu=Application.getMenu(),
                           operating_system_front=operating_system,
                           user_agent_front=request.user_agent,
                           version_front=version,
                           local_time_front=local_time
                           )


@app.route('/')
def index():
    return render_template("main.html",
                           menu=Application.getMenu(),
                           operating_system_front=operating_system,
                           user_agent_front=request.user_agent,
                           version_front=version,
                           local_time_front=local_time
                           )


@app.route("/about")
def about():
    return render_template("about.html",
                           menu=Application.getMenu(),
                           operating_system_front=operating_system,
                           user_agent_front=request.user_agent,
                           version_front=version,
                           local_time_front=local_time,
                           is_show_about_me_front=is_show_about_me
                           )


@app.route("/contacts")
def score():
    return render_template("contacts.html",
                           menu=Application.getMenu(),
                           operating_system_front=operating_system,
                           user_agent_front=request.user_agent,
                           version_front=version,
                           local_time_front=local_time
                           )


if __name__ == '__main__':
    app.run(debug=True)
