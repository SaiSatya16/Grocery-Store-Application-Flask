from flask_restful import Resource, Api, fields, marshal_with, reqparse
from model import db
from model import Product, Category, Association

from werkzeug.exceptions import HTTPException
from flask_cors import CORS
import json
from flask import make_response
import os
api = Api()

#==========================Validation========================================================
class NotFoundError(HTTPException):
    def __init__(self,status_code):
        self.response = make_response(" ", status_code)

class BusinessValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"error_code":error_code,"error_message":error_message}
        self.response = make_response(json.dumps(message), status_code)


#==============================output fields========================================
Category_fields = {
    "id":fields.Integer,
    "name":fields.String
}

Product_fields = {
    "id":fields.Integer,
    "name":fields.String,
    "unit":fields.String,
    "rate":fields.Integer,
    "quantity":fields.Integer,
    "manufacture_date":fields.String,
    "expiry_date":fields.String,
    "category_id": fields.Integer
}

#====================Create Category and product request pares=======================================
create_Category_parser = reqparse.RequestParser()
create_Category_parser.add_argument('name')

create_product_parser = reqparse.RequestParser()
create_product_parser.add_argument('name')
create_product_parser.add_argument('unit')
create_product_parser.add_argument('rate')
create_product_parser.add_argument('quantity')
create_product_parser.add_argument('manufacture_date')
create_product_parser.add_argument('expiry_date')
create_product_parser.add_argument('category_id')

#====================Update Category and product request pares=======================================
update_Category_parser = reqparse.RequestParser()
update_Category_parser.add_argument('name')

update_product_parser = reqparse.RequestParser()
update_product_parser.add_argument('name')
update_product_parser.add_argument('unit')
update_product_parser.add_argument('rate')
update_product_parser.add_argument('quantity')
update_product_parser.add_argument('manufacture_date')
update_product_parser.add_argument('expiry_date')
update_product_parser.add_argument('category_id')


#=================================Category api======================================================
class Category_Api(Resource):
    #==========GET================
    @marshal_with(Category_fields)
    def get(self,id):
        category = Category.query.filter_by(id = id).first()
        if category is None:
            return NotFoundError(status_code=404)
        else:
            return category
    #==========POST================   
    @marshal_with(Category_fields)
    def post(self):
        args = create_Category_parser.parse_args()
        name = args.get("name",None)
        if name is None:
            raise BusinessValidationError(status_code=400,error_code="BE1001",error_message="Category name is required")
        category = Category.query.filter_by(name = name).first()
        if category:
            raise BusinessValidationError(status_code=400,error_code="BE1004",error_message="duplicate Category")
        new_Category = Category(name=name)
        db.session.add(new_Category)
        db.session.commit()
        return new_Category,201
    
    #==========PUT================
    @marshal_with(Category_fields)
    def put(self,id):
        args = update_Category_parser.parse_args()
        name = args.get("name")
        if name is None:
            return BusinessValidationError(status_code=400, error_code="name", error_message="Category Name is required")
        category = Category.query.filter_by(id = id).first()
        if category is None:
            raise NotFoundError(status_code=404)
        Category.query.filter(Category.id==id).update({'name':name})
        db.session.commit()
        return category
    
    #================DELETE===========
    def delete(self,id):
        C1 = Category.query.get(id)
        if C1 is not None:
            p1 = C1.product_relation 
            for i in p1:
                db.session.delete(i)
            db.session.delete(C1)
            db.session.commit()
            return "deleted Category",201
        return NotFoundError(status_code=404)

#=================================Product api======================================================
class Product_Api(Resource):
    #==========GET================
    @marshal_with(Product_fields)
    def get(self,id):
        product = Product.query.filter_by(id = id).first()
        if product is None:
            return NotFoundError(status_code=404)
        else:
            return product
    #==========POST================   
    @marshal_with(Product_fields)
    def post(self):
        args = create_product_parser.parse_args()
        name = args.get("name",None)
        unit = args.get("unit",None)
        rate = args.get("rate",None)
        quantity = args.get("quantity",None)
        manufacture_date = args.get("manufacture_date",None)
        expiry_date = args.get("expiry_date",None)
        category_id = args.get("category_id",None)
        if name is None:
            raise BusinessValidationError(status_code=400,error_code="BE1001",error_message="Category name is required")
        if unit is None:
            raise BusinessValidationError(status_code=400,error_code="BE1002",error_message="Category unit is required")
        if rate is None:
            raise BusinessValidationError(status_code=400,error_code="BE1003",error_message="Category rate is required")
        if quantity is None:
            raise BusinessValidationError(status_code=400,error_code="BE1008",error_message="Category quantity is required")
        if manufacture_date is None:
            raise BusinessValidationError(status_code=400,error_code="BE1005",error_message="Category manufacture_date is required")
        if expiry_date is None:
            raise BusinessValidationError(status_code=400,error_code="BE1006",error_message="Category expiry_date is required")
        if category_id is None:
            raise BusinessValidationError(status_code=400,error_code="BE1007",error_message="Category category_id is required")
     
        
        product = Product.query.filter_by(name = name, unit= unit, rate= rate, quantity= quantity, manufacture_date=manufacture_date, category_id=category_id).first()
        if product:
            raise BusinessValidationError(status_code=400,error_code="BE1004",error_message="duplicate Product")
        new_Product = Product(name=name, unit= unit, rate= rate, quantity= quantity, manufacture_date=manufacture_date, expiry_date=expiry_date, category_id=category_id)
        
        db.session.add(new_Product)
        db.session.commit()
        p = Product.query.filter_by(name = name, unit= unit, rate= rate, quantity= quantity, manufacture_date=manufacture_date, category_id=category_id).first()
        pid = p.id
        asso = Association(category_id=category_id,product_id=pid)
        db.session.add(asso)
        db.session.commit()
        return new_Product,201
    
    #==========PUT================
    @marshal_with(Product_fields)
    def put(self,id):
        args = update_product_parser.parse_args()
        name = args.get("name",None)
        unit = args.get("unit",None)
        rate = args.get("rate",None)
        quantity = args.get("quantity",None)
        manufacture_date = args.get("manufacture_date",None)
        expiry_date = args.get("expiry_date",None)
        category_id = args.get("category_id",None)
        if name is None:
            raise BusinessValidationError(status_code=400,error_code="BE1001",error_message="Category name is required")
        if unit is None:
            raise BusinessValidationError(status_code=400,error_code="BE1002",error_message="Category unit is required")
        if rate is None:
            raise BusinessValidationError(status_code=400,error_code="BE1003",error_message="Category rate is required")
        if quantity is None:
            raise BusinessValidationError(status_code=400,error_code="BE1008",error_message="Category quantity is required")
        if manufacture_date is None:
            raise BusinessValidationError(status_code=400,error_code="BE1005",error_message="Category manufacture_date is required")
        if expiry_date is None:
            raise BusinessValidationError(status_code=400,error_code="BE1006",error_message="Category expiry_date is required")
        if category_id is None:
            raise BusinessValidationError(status_code=400,error_code="BE1007",error_message="Category category_id is required")
     
        product = Product.query.filter_by(id = id).first()
        if product is None:
            raise NotFoundError(status_code=404)
        Product.query.filter(Product.id==id).update({'name':name,'unit':unit, 'rate':rate, 'quantity': quantity, 'manufacture_date':manufacture_date, 'expiry_date':expiry_date, 'category_id':category_id})
        db.session.commit()
        return product
    
    #================DELETE===========
    def delete(self,id):
        p1 = Product.query.get(id)
        if p1 is not None:
            Product.query.filter_by(id = id).delete()
            db.session.commit()
            Association.query.filter_by(product_id = id).delete()
            db.session.commit()
            return "deleted Product",201
        return NotFoundError(status_code=404)  

api.add_resource(Category_Api, "/api/category/<int:id>", "/api/category")
api.add_resource(Product_Api, "/api/product/<int:id>", "/api/product")