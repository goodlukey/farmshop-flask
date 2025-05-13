# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField('商品名稱', validators=[DataRequired()])
    price = FloatField('價格', validators=[DataRequired()])
    description = TextAreaField('商品敘述')
    image = FileField('商品圖片')  # 圖片不是必填
    submit = SubmitField('新增商品')

class MarketForm(FlaskForm):
    name = StringField('市集名稱', validators=[DataRequired()])
    location = StringField('地點', validators=[DataRequired()])
    date = StringField('時間')  # 非必填
    market_link = StringField('市集網站連結')
    map_link = StringField('Google 地圖連結')
    submit = SubmitField('新增市集')
