from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, Regexp, EqualTo


class Form(FlaskForm):
    login = StringField('* Login *',
                        validators=[InputRequired('Login is required')])

    # This is for do lines little bit shorter to regards PEP8
    _0 = 'Password is required'
    _1 = 'Minimal length for password 6'
    _2 = 'Passwords must match'
    _3 = 'Number is required'
    _4 = 'Length of number must be equal to 7'
    _5 = 'It must be only digits'
    _6 = 'Length of PIN must be equal to 4'
    _7 = 'PIN is required'
    _8 = 'It must be by template: XX (for < 2015), or X00 (for >= 2015)'
    _9 = 'Length must be by 8 (for < 2015), or 6 (for >= 2015)'

    password = PasswordField('* Password *',
                             validators=[InputRequired(_0),
                                         Length(min=6, message=_1)])

    password_r = PasswordField('* Password repean *',
                               validators=[InputRequired(_0),
                                           Length(min=6, message=_1),
                                           EqualTo('password', message=_2)])

    e_number = StringField('* Number *',
                           validators=[InputRequired(_3),
                                       Length(min=7, max=7, message=_4),
                                       Regexp(regex='^[0-9]+$', message=_5)])

    e_pin = PasswordField('* PIN *',
                          validators=[InputRequired(_7),
                                      Length(min=4, max=4, message=_6),
                                      Regexp(regex='^[0-9]+$', message=_5)])

    e_year = SelectField('* Year *', choices=[2013, 2014, 2015,
                                              2016, 2017, 2018,
                                              2019, 2020, 2021])
    d_series = StringField('Series')
    d_number = StringField('* Number *')
