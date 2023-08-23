import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

import json
from datetime import date



Base = declarative_base()

class Category(Base):
    __tablename__ = "category"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f' {self.id}: {self.name}'
    
class Product(Base):
    __tablename__ = "product"
    id = sq.Column(sq.Integer, primary_key=True)
    name =  sq.Column(sq.String(length=40), unique=True)
    unit = sq.Column(sq.String(length=10))
    category_id = sq.Column(sq.Integer, sq.ForeignKey("category.id"))
    
    category = relationship(Category, backref="products")

    def __str__(self):
        return f'{self.name} ({self.unit})'

class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name =  sq.Column(sq.String(length=40), unique=True)
    adress = sq.Column(sq.String(length=150),nullable=True)

    def __str___(self):
        return f'{self.id}: {self.name} по адресу {self.adress}'

class Sl_template(Base):
    __tablename__ = "sl_template"
    id = sq.Column(sq.Integer, primary_key=True)
    name =  sq.Column(sq.String(length=40), unique=True)
    comment = sq.Column(sq.String(length=150),nullable=True)

    def __str__(self):
        return f'{self.id}: {self.name}'

class Sl_template_pruduct(Base):
    __tablename__ = "sl_temptale_product"
    id = sq.Column(sq.Integer, primary_key=True)
    sl_template_id = sq.Column(sq.Integer, sq.ForeignKey("sl_template.id"), nullable=False)
    product_id = sq.Column(sq.Integer, sq.ForeignKey("product.id"), nullable=False)
    amount = sq.Column(sq.Numeric, nullable=False)

class Shopping_list(Base):
    __tablename__ = "shopping_list"
    id = sq.Column(sq.Integer, primary_key=True)
    date =  sq.Column(sq.Date)
    comment = sq.Column(sq.String(length=150),nullable=True)
    s_l_template = sq.Column(sq.Integer,sq.ForeignKey("sl_template.id"),nullable=True)

class Shopping_list_product(Base):
    __tablename__ = "shopping_list_product"
    id = sq.Column(sq.Integer, primary_key=True)
    shopping_list_id = sq.Column(sq.Integer, sq.ForeignKey("shopping_list.id"), nullable=False)
    product_id = sq.Column(sq.Integer, sq.ForeignKey("product.id"), nullable=False)
    amount = sq.Column(sq.Numeric, nullable=False)

class Product_Shop(Base):
    __tablename__ = 'product_shop'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    product_id = sq.Column(sq.Integer, sq.ForeignKey("product.id"), nullable=False)
    price = sq.Column(sq.Numeric)

class Purchased_product(Base):
    __tablename__ = "purchased_products"
    id = sq.Column(sq.Integer, primary_key=True)
    product_id =  sq.Column(sq.Integer, sq.ForeignKey("product.id"))
    amount = sq.Column(sq.Numeric)
    date = sq.Column(sq.Date)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey("shop.id"))
    shopping_list_id = sq.Column(sq.Integer, sq.ForeignKey("shopping_list.id"), nullable=True)
    price = sq.Column(sq.Numeric, nullable=True)
