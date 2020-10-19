from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.core import SelectField


class UpdateForm(FlaskForm):
    
    nameToChange = SelectField('Username to change:')
    newUsername = StringField('Username:', validators=[DataRequired()])
        
    newPassword = PasswordField('Password:', validators=[DataRequired()])
    newRole = BooleanField("Is the user Admin?", false_values=(False, 'false', 0, '0'))
    
    submit = SubmitField('Update')
