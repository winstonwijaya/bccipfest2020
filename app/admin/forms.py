# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, InputRequired


class ParticipantForm(FlaskForm):
    """
    Form for admin to add or edit a participant
    """
    partname = StringField('Participant', validators=[DataRequired()])
    fcd = StringField('MFD', validators=[InputRequired()])
    usd = StringField('USD', validators=[InputRequired()])
    sar = StringField('SAR', validators=[InputRequired()])
    rub = StringField('RUB', validators=[InputRequired()])
    yen = StringField('YEN', validators=[InputRequired()])
    submit = SubmitField('Submit')

class StorageForm(FlaskForm):
    """
    Form for admin to add or edit a storage
    """
    storown = StringField('Participant', validators=[DataRequired()])
    stornum = IntegerField('StorageNumber', validators=[InputRequired()])
    current_capacity = IntegerField('CurrentFill', validators=[InputRequired()])
    submit = SubmitField('Submit')