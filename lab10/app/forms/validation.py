from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, Regexp


def validate(form: FlaskForm):
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
