from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField,\
    SelectField, SubmitField, BooleanField
from wtforms.validators import Length, InputRequired, Regexp, NumberRange
from wtforms.widgets.html5 import NumberInput


class GoodsForm(FlaskForm):
    code = StringField('Code of goods',
                       validators=[InputRequired(),
                                   Length(min=10, max=12),
                                   Regexp('^[A-Za-z0-9_-]+$')])
    name = StringField('Name',
                       validators=[InputRequired(), Length(min=2, max=60)])
    category = SelectField('Category', validators=[InputRequired()])
    is_available = BooleanField('Is available on storage',
                                validators=[], default=False)
    count = IntegerField('Count in storage', widget=NumberInput(),
                         validators=[InputRequired(), NumberRange(min=0)],
                         default=0)
    price = IntegerField('Price', widget=NumberInput(),
                         validators=[InputRequired(), NumberRange(min=0)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    submit = SubmitField('')


class CategoryGoodsForm(FlaskForm):
    name = StringField('Name',
                       validators=[InputRequired(), Length(min=2, max=50)])
    submit = SubmitField('')
