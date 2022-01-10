from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, \
    SelectField, SubmitField, SelectMultipleField
from wtforms.validators import Length, InputRequired
from flask_wtf.file import FileField, FileAllowed


class PostForm(FlaskForm):
    title = StringField('Title of post',
                        validators=[InputRequired(), Length(min=2, max=60)])
    text = TextAreaField('Text of post', validators=[Length(max=500)])
    image = FileField('Post Picture', validators=[FileAllowed(['jpg', 'png'])])
    category = SelectField('Category', validators=[InputRequired()])
    tags = SelectMultipleField("Tags",
                               validators=[InputRequired()], coerce=int)
    submit = SubmitField('')


class CategoryForm(FlaskForm):
    name = StringField('Name',
                       validators=[InputRequired(), Length(min=2, max=50)])
    submit = SubmitField('')
