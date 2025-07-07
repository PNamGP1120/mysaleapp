from saleapp import app, login
from flask import render_template, request, url_for, redirect, session, jsonify
import utils
import math
import cloudinary.uploader
from flask_login import login_user, logout_user

@app.route('/')
def home():
    category_id = request.args.get('category_id', type=int)
    keyword = request.args.get('keyword', type=str)
    page = request.args.get('page', type=int, default=1)
    products = utils.load_products(category_id = category_id, 
                                   keyword=keyword,
                                   page=page
                                   )
    
    counter = utils.count_products()
    return render_template('index.html', 
                           products=products,
                           pages=math.ceil(counter / app.config['PAGE_SIZE']),
                           )

@app.route('/register', methods=['GET', 'POST'])
def user_register():
    err_msg = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        email = request.form.get('email', '').strip()
        full_name = request.form.get('full_name', '').strip()

        # Kiểm tra dữ liệu đầu vào
        if not all([username, password, confirm_password, email, full_name]):
            err_msg = "Vui lòng điền đầy đủ thông tin"
        elif len(username) < 3:
            err_msg = "Tên đăng nhập phải có ít nhất 3 ký tự"
        elif len(password) < 6:
            err_msg = "Mật khẩu phải có ít nhất 6 ký tự"
        elif password != confirm_password:
            err_msg = "Mật khẩu không khớp"
        elif '@' not in email or '.' not in email:
            err_msg = "Email không hợp lệ"
        # elif utils.check_username_exists(username):
        #     err_msg = "Tên đăng nhập đã tồn tại"
        # elif utils.check_email_exists(email):
        #     err_msg = "Email đã được sử dụng"
        else:
            try:
                avatar = request.files.get('avatar')
                if avatar:
                    avatar_path = cloudinary.uploader.upload(avatar).get('secure_url')

                utils.add_user(
                    username=username,
                    password=password,
                    email=email,
                    full_name=full_name,
                    avatar=avatar_path if avatar else None
                )
                return redirect(url_for('user_signin'))
            except Exception as e:
                err_msg = f"Đăng ký thất bại: {e}"
    return render_template('register.html', err_msg=err_msg)

@app.route('/user-login', methods=['GET', 'POST'])
def user_signin():
    err_msg = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = utils.check_login(username, password)
        if user:
            login_user(user = user, remember=True)
            return redirect(url_for('home'))
        else:
            err_msg = "Tên đăng nhập hoặc mật khẩu không đúng"
       
    return render_template('login.html', err_msg=err_msg)

@app.route('/user-signout')
def user_signout():
    """
    Handles user sign out by clearing the session and redirecting to the home page.
    """
    logout_user()
    return redirect(url_for('home'))

@app.context_processor
def common_response():
    categories = utils.load_categories()
    return {
        'categories': categories,
        'page_size': app.config['PAGE_SIZE'],
    }

@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id)

@app.route('/products')
def product_list():
    category_id = request.args.get('category_id', type=int)
    keyword = request.args.get('keyword', type=str)
    from_price = request.args.get('from_price', type=float)
    to_price = request.args.get('to_price', type=float)

    products = utils.load_products(category_id,
                                   keyword=keyword,
                                   from_price=from_price,
                                   to_price=to_price)
    return render_template('products.html', 
                           products=products, 
                           )

@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = utils.get_product_by_id(product_id)
    if product is None:
        return "Product not found", 404
    return render_template('product_detail.html', 
                           product=product)

@app.route('/api/add-cart', methods=['POST'])
def add_to_cart(product_id):
    """
    Adds a product to the shopping cart stored in the session.
    """
    id =''
    name =''
    price = ''

    import pdb
    pdb.set_trace()
    
    cart = session.get('cart', {})
    if product_id in cart:
        cart[product_id]['quantity'] = cart[product_id]['quantity'] + 1
    else:
        cart[product_id] = {
            'id': product_id,
            'name': request.form.get('name', ''),
            'price': request.form.get('price', type=float, default=0.0),
            'quantity': 1,
        }
    session['cart'] = cart
    return jsonify(utils.count_cart(cart)), 200


if __name__ == '__main__':
    from saleapp.admin import *
    app.run(debug=True)