from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    username = db.Column(db.String,primary_key = True,unique = True,nullable = False)
    email = db.Column(db.String,nullable = False,unique = True)
    password = db.Column(db.String,nullable = False)

class Admin(db.Model):
    username = db.Column(db.String,primary_key = True,unique = True,nullable = False)
    password = db.Column(db.String,nullable = False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    name = db.Column(db.String(100), nullable=False)
    product_relation = db.relationship("Product",backref="category_relation", secondary="association") 

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    name = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(100), nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    manufacture_date = db.Column(db.String(100), nullable=False)
    expiry_date = db.Column(db.String(100), nullable=False)
    category_id=db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    name = db.Column(db.String(100), nullable=False)
    product_id=db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    product_name=db.Column(db.String(100), nullable=False)
    req_quantity = db.Column(db.Integer,nullable = False)
    product_rate=db.Column(db.Integer, nullable=False)
    product_unit=db.Column(db.String(100),  nullable=False)

class Bought(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    name = db.Column(db.String(100), nullable=False)
    product_id=db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    product_name=db.Column(db.String(100), nullable=False)
    req_quantity = db.Column(db.Integer,nullable = False)
    product_rate=db.Column(db.Integer, nullable=False)
    product_unit=db.Column(db.String(100),  nullable=False)
    




class Association(db.Model):
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"),primary_key = True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"),primary_key = True, nullable=False)
