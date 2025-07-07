from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import cloudinary
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!safhgoisugd@$#%$@%#$@#$!@fuaysgvbdcfauyo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/saleapp?charset=utf8mb4' % quote('Phuongnam0212@')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PAGE_SIZE'] = 4
cloudinary.config(
    cloud_name="dqpu49bbo",
    api_key="743773348627895",
    api_secret="EF7elKsibuI8JEBqfMNZYYWUYvo",
    secure=True
)
db = SQLAlchemy(app)
login = LoginManager(app)

