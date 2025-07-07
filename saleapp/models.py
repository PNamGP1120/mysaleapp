from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from saleapp import db, app
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin

class BaseModel(db.Model):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"
    
class UserRole(UserEnum):
    ADMIN = 1
    USER = 2
    
class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    avatar = Column(String(100), nullable=True)
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    def __str__(self):
        return self.username
    

class Category(BaseModel):
    __tablename__ = 'category'
    
    name = Column(String(100), nullable=False)
    
    products = relationship('Product', back_populates='category', lazy=False)
    def __repr__(self):
        return f"<Category {self.name}>"
    
    def __str__(self):
        return self.name

    
class Product(BaseModel):
    __tablename__ = 'product'
    
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    image = Column(String(100), nullable=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship('Category', back_populates='products')
    
    def __repr__(self):
        return f"<Product {self.name}>"
    
    def __str__(self):
        return self.name
    
if __name__ == '__main__':
    with app.app_context():
        # p = Product.query.first()
        # print(p.category)
        db.create_all()
        # print("Database tables created successfully.")
        # Example of adding a new category
        # c1 = Category(name='Điện thoại')
        # c2 = Category(name='Máy tính bảng')
        # c3 = Category(name='Laptop')
        # c4 = Category(name='Đồng hồ thông minh')
        # c5 = Category(name='Phụ kiện')
        # db.session.add_all([c1, c2, c3, c4, c5])
        # db.session.commit()
        # print("Categories added successfully.")

        # products = utils.load_products()
        #
        # for p in products:
        #     product = Product(
        #         name=p['name'],
        #         description=p['description'],
        #         price=p['price'],
        #         image=p['image'],
        #         category_id=p['category_id']
        #     )
        #     db.session.add(product)
        # db.session.commit()
        # print("Products added successfully.")