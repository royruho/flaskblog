from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class ReminderForm(FlaskForm):
    title = StringField('Title of Reminder', validators=[DataRequired()])
    duration_sec = IntegerField('Time in seconds for Reminder Delay',
                                validators=[DataRequired(),
                                            NumberRange(min=0, max=100)])
    submit = SubmitField('Submit')
