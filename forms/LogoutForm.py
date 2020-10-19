from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField


class LogoutForm(FlaskForm):
    logoutBtn = SubmitField("Sign out")
