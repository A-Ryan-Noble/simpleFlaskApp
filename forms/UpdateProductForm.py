from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, InputRequired
from wtforms.fields.core import SelectField, DecimalField
from flask_wtf.file import FileField, file_required
from flask_wtf.html5 import NumberInput


class UpdateProductForm(FlaskForm):
    productOwner = SelectField('Username of owner:', validators=[DataRequired()])

    productName = StringField('Product name:', validators=[DataRequired()])

    imageFile = FileField("Product Image", validators=[file_required()])

    productPrice = DecimalField("Product price:", widget=NumberInput(0.01, 0.01), validators=[DataRequired()])

    update = SubmitField('Update Product')
