from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Product, Category, User

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username udah di pake brooo', 'danger')
            return redirect(url_for('register'))
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrasi berhasil silahkan login bang', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            flash('Login sukses cuy', 'success')
            return redirect(url_for('index'))
        else:
            flash('username dan password salah bang', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Kamu telah logout bang', 'info')
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user_id' not in session:
        flash('Login dulu lah bang', 'warning')
        return redirect(url_for('login'))

    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    categories = Category.query.all()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        stock = request.form['stock']
        category_id = request.form['category']

        if not price.isnumeric() or not stock.isnumeric():
            flash('Harga dan stok harus angka bang', 'danger')
            return redirect(url_for('add_product'))

        new_product = Product(name=name, description=description, price=int(price), stock=int(stock), category_id=category_id)
        db.session.add(new_product)
        db.session.commit()
        flash('Produk telah sukses di tambahkan ditoko bang', 'success')
        return redirect(url_for('index'))

    return render_template('add_product.html', categories=categories)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    categories = Category.query.all()

    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        product.stock = request.form['stock']
        product.category_id = request.form['category']

        if not product.price.isnumeric() or not product.stock.isnumeric():
            flash('Harga dan stok harus angka bang', 'danger')
            return redirect(url_for('edit_product', id=product.id))

        db.session.commit()
        flash('Produk telah di update bang', 'success')
        return redirect(url_for('index'))

    return render_template('edit_product.html', product=product, categories=categories)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Produk telah di hapus bang', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
