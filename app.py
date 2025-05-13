# app.py
from flask import Flask, render_template
from models import db, Product, Market
import os
from flask import request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from forms import ProductForm, MarketForm

app = Flask(__name__)
app.secret_key = 'your-secret-key'
UPLOAD_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 設定資料庫位置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化資料庫
db.init_app(app)

# 建立資料庫與表（第一次啟動時執行）
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def product_list():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        filename = ''
        if form.image.data:
            image_file = form.image.data
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)

        new_product = Product(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            image_url=f'/static/images/{filename}' if filename else ''
        )
        db.session.add(new_product)
        db.session.commit()
        flash('商品新增成功！')
        return redirect(url_for('product_list'))

    return render_template('add_product.html', form=form)

@app.route('/markets')
def market_info():
    markets = Market.query.all()
    return render_template('markets.html', markets=markets)

@app.route('/add-market', methods=['GET', 'POST'])
def add_market():
    form = MarketForm()
    if form.validate_on_submit():
        new_market = Market(
            name=form.name.data,
            location=form.location.data,
            date=form.date.data,
            market_link=form.market_link.data,
            map_link=form.map_link.data
        )
        db.session.add(new_market)
        db.session.commit()
        flash('市集新增成功！')
        return redirect(url_for('market_info'))

    return render_template('add_market.html', form=form)

@app.route('/delete-product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('商品已刪除')
    return redirect(url_for('product_list'))

@app.route('/delete-market/<int:market_id>', methods=['POST'])
def delete_market(market_id):
    market = Market.query.get_or_404(market_id)
    db.session.delete(market)
    db.session.commit()
    flash('市集已刪除')
    return redirect(url_for('market_info'))

if __name__ == '__main__':

    # 初始化資料一次用，新增一些商品
    with app.app_context():
        if not Product.query.first():
            sample_products = [
                Product(name='有機小黃瓜', price=35, description='新鮮採收的小黃瓜', image_url=''),
                Product(name='手工果醬', price=120, description='無添加純果肉果醬', image_url=''),
            ]
            db.session.add_all(sample_products)
            db.session.commit()

        if not Market.query.first():
            sample_markets = [
                Market(
                    name='台北希望市集',
                    location='台北市中正區北平東路 31 號(華山藝文特區旁)',
                    date='星期六 10：00 ～ 19：00 / 星期日 10：00 ～ 18：00',
                    market_link='https://www.ehope.org.tw/'
                ),
                Market(
                    name='台北花博農民市集',
                    location='圓山捷運站1號出口',
                    date='週末假日 10:00~18:00',
                    market_link='https://www.expofarmersmarket.gov.taipei/index2.php'
                ),
            ]
            db.session.add_all(sample_markets)
            db.session.commit()
    app.run(debug=True)


