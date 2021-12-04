from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import Length, InputRequired
from flask_wtf.file import FileField, FileAllowed


class PostForm(FlaskForm):
    title = StringField('Title of post', validators=[InputRequired(), Length(min=2, max=60)])
    text = TextAreaField('Text of post', validators=[Length(max=500)])
    image = FileField('Post Picture', validators=[FileAllowed(['jpg', 'png'])])
    type = SelectField('Type', choices=[('News', 'News'), ('Publication', 'Publication'), ('Other', 'Other')])
    submit = SubmitField('')
