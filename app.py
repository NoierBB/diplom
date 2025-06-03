from flask import Flask, render_template, request, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os
from flask import session as flask_session
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'your_secret_key_here'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Инициализация базы данных ДО создания моделей
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/admin/add-product', methods=['GET', 'POST'])
def add_product():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        category = request.form['category']
        
        # Обработка загрузки изображения
        image = request.files['image']
        filename = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        new_product = Product(
            name=name,
            price=price,
            description=description,
            image=filename,
            category=category
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/dashboard.html')

@app.route('/admin/edit-product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.description = request.form['description']
        product.category = request.form['category']
        
        image = request.files['image']
        if image and allowed_file(image.filename):
            # Удаляем старое изображение, если есть
            if product.image:
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], product.image))
                except:
                    pass
            
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product.image = filename
        
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/edit_product.html', product=product)

@app.route('/admin/delete-product/<int:id>', methods=['POST'])
def delete_product(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    product = Product.query.get_or_404(id)
    
    # Удаляем изображение, если есть
    if product.image:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], product.image))
        except:
            pass
    
    db.session.delete(product)
    db.session.commit()
    
    return redirect(url_for('admin_dashboard'))

# Модель товара
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(100))
    category = db.Column(db.String(50))

# Удалите before_request - используйте Flask-Migrate вместо этого
# Или, если хотите оставить автоматическое создание:
@app.before_request
def create_tables():
    with app.app_context():
        db.create_all()

# Создаём команду для инициализации БД
@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    db.create_all()
    print("База данных создана")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/catalog')
def catalog():
    return redirect(url_for('products'))

# Один маршрут для продуктов (удалите дубликат)
@app.route('/products')
def products():
    # Получаем параметр категории из URL
    category = request.args.get('category')
    
    # Фильтруем товары по категории, если указана
    if category:
        products_list = Product.query.filter_by(category=category).all()
    else:
        products_list = Product.query.all()
    
    # Получаем список всех категорий для фильтра
    categories = db.session.query(Product.category).distinct().all()
    
    return render_template('products.html', 
                         products=products_list,
                         categories=categories,
                         current_category=category)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Проверка учетных данных (в реальном приложении используйте хеширование!)
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin/login.html', error='Неверные учетные данные')
    
    return render_template('admin/login.html')

# Защищенный маршрут админ-панели
@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    category_filter = request.args.get('category', default=None)
    
    # Фильтрация товаров
    if category_filter:
        products = Product.query.filter_by(category=category_filter).all()
    else:
        products = Product.query.all()
    
    # Получаем список всех категорий для фильтра
    categories = db.session.query(Product.category).distinct().all()
    
    return render_template('admin/dashboard.html', 
                         products=products,
                         categories=categories,
                         current_category=category_filter)

    
    # return render_template('admin/dashboard.html')

# Выход из админки
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

# Товары в корзине будут храниться в сессии
@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    
    product = Product.query.get_or_404(product_id)
    
    # Инициализируем корзину в сессии, если её нет
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    
    # Добавляем товар в корзину
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image': product.image,
            'category': product.category
        }
    
    # Сохраняем обновленную корзину в сессии
    session['cart'] = cart
    
    # Возвращаем JSON-ответ для AJAX
    return {
        'success': True,
        'cart_total': sum(item['quantity'] for item in cart.values())
    }

@app.route('/cart')
def view_cart():
    cart = flask_session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('cart.html', cart=cart, total=total)

@app.route('/update-cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    action = request.form.get('action')
    cart = flask_session.get('cart', {})
    
    if str(product_id) in cart:
        if action == 'increase':
            cart[str(product_id)]['quantity'] += 1
        elif action == 'decrease':
            if cart[str(product_id)]['quantity'] > 1:
                cart[str(product_id)]['quantity'] -= 1
            else:
                del cart[str(product_id)]
        elif action == 'remove':
            del cart[str(product_id)]
    
    flask_session['cart'] = cart
    return redirect(url_for('view_cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Здесь будет обработка оформления заказа
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        
        # Создаем заказ в БД (нужно добавить модель Order)
        # order = Order(name=name, email=email, address=address, ...)
        # db.session.add(order)
        # db.session.commit()
        
        # Очищаем корзину
        flask_session.pop('cart', None)
        
        return render_template('order_success.html')
    
    cart = flask_session.get('cart', {})
    if not cart:
        return redirect(url_for('view_cart'))
    
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('checkout.html', cart=cart, total=total)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)