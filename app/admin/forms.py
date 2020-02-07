# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class ParticipantForm(FlaskForm):
    """
    Form for admin to add or edit a participant
    """
    partname = StringField('Participant', validators=[DataRequired()])
    fcd = IntegerField('FCD', validators=[DataRequired()])
    usd = IntegerField('USD', validators=[DataRequired()])
    sar = IntegerField('SAR', validators=[DataRequired()])
    rub = IntegerField('RUB', validators=[DataRequired()])
    yen = IntegerField('YEN', validators=[DataRequired()])
    submit = SubmitField('Submit')

class StorageForm(FlaskForm):
    """
    Form for admin to add or edit a storage
    """
    storown = StringField('Participant', validators=[DataRequired()])
    stornum = IntegerField('StorageNumber', validators=[DataRequired()])
    current_capacity = IntegerField('CurrentFill', validators=[DataRequired()])
    submit = SubmitField('Submit')