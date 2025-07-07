# import json, os
# from saleapp import app
from saleapp import app, db
from saleapp.models import Category, Product, User
import hashlib

# def read_json_file(file_path):
#     """
#     Reads a JSON file and returns its content as a dictionary.
#
#     :param file_path: Path to the JSON file.
#     :return: Dictionary containing the JSON data.
#     """
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             return json.load(file)
#     except FileNotFoundError:
#         print(f"File {file_path} not found.")
#         return {}
#     except json.JSONDecodeError:
#         print(f"Error decoding JSON from the file {file_path}.")
#         return {}
    
def load_categories():  
    return Category.query.all()

def load_products(category_id=None, keyword=None, from_price=None, to_price=None, page=1):
    """
    Loads products from the database with optional filters.
    
    :param category_id: Filter by category ID.
    :param keyword: Search keyword for product name or description.
    :param from_price: Minimum price filter.
    :param to_price: Maximum price filter.
    :return: List of products matching the filters.
    """
    query = Product.query.filter(Product.active.is_(True)) 
    
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    if keyword:
        query = query.filter((Product.name.contains(keyword)) | (Product.description.contains(keyword)))
    
    if from_price is not None:
        query = query.filter(Product.price >= from_price)
    
    if to_price is not None:
        query = query.filter(Product.price <= to_price)
    
    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size
    return query.slice(start, end).all()

def count_products():
    """
    Counts the total number of products in the database.
    
    :return: Total count of products.
    """
    return Product.query.filter(Product.active.is_(True)).count()

def get_product_by_id(product_id):
    """
    Retrieves a product by its ID.
    
    :param product_id: ID of the product to retrieve.
    :return: Product dictionary if found, otherwise None.
    """
    products = load_products()
    return next((p for p in products if p['id'] == product_id), None)

def add_user(username, password, email, full_name=None, **kwargs):
    """
    Adds a new user to the database.
    
    :param username: Username of the user.
    :param password: Password of the user.
    :param email: Email of the user.
    :param full_name: Full name of the user (optional).
    :return: User object if added successfully, otherwise None.
    """

    password = hashlib.md5(password.encode()).hexdigest()
    new_user = User(username=username, 
                    password=password, 
                    email=email, 
                    full_name=full_name, 
                    avatar=kwargs.get('avatar', None))
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        print(f"Error adding user: {e}")
        return None

def check_login(username, password):
    """
    Checks if the user credentials are valid.
    
    :param username: Username of the user.
    :param password: Password of the user.
    :return: User object if credentials are valid, otherwise None.
    """
    if not username or not password:
        return None
    password = hashlib.md5(password.encode()).hexdigest()
    return User.query.filter_by(username=username, password=password).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def count_cart(cart):
    """
    Counts the total number of items in the cart.
    
    :param cart: Dictionary representing the shopping cart.
    :return: Total count of items in the cart.
    """
    total_quantity, total_amount = 0, 0
    if cart:
        for item in cart.values():
            total_quantity += item['quantity']
            total_amount += item['quantity'] * item['price']
    return total_quantity, total_amount

if __name__ == '__main__':
    with app.app_context():
        print(load_categories())