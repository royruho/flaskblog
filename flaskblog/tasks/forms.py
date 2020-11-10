from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    duration_sec = IntegerField('Duration', validators=[DataRequired(),
                                                        NumberRange(min=0,
                                                                    max=100)])
    submit = SubmitField('Submit')
