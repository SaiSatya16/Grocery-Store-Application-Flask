from flask import Flask, render_template ,request,redirect, url_for
from model import *
import os
from api import *
from flask_cors import CORS

#==============================configuration===============================

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
CORS(app)
api.init_app(app)
db.init_app(app)
app.app_context().push()

#==============================Controllers=================================

@app.route('/',methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/about',methods=['GET','POST'])
def about():
    return render_template('about.html')

#==============================Login=================================
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        a = request.form['username']
        b = request.form['password']
        y = User.query.all()
        l = [] 
        for i in y:
           l.append((i.username,i.password))
        if a == "admin" and b == "admin123":
            return render_template("you_are_admin.html")
        elif (a,b) in l:
            return redirect(url_for('user_dashboard',id = a))
        else:
            return redirect('/unsuccessful')


#==============================Signup=================================
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        a = request.form['username']
        b = request.form['password']
        c = request.form['email']
        user_record = User(username=a, email=c, password=b)
        y = User.query.all()
        l = []
        for i in y:
            l.append(i.username)
        if a in l:
            return redirect('/success')
        else:
            db.session.add(user_record)
            db.session.commit()
            return redirect('/success')


#==============================Admin Login=================================
@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    if request.method == "GET":
        return render_template("adminlogin.html")
    elif request.method == "POST":
        a = request.form['adminUsername']
        b = request.form['adminPassword']
        y = Admin.query.all()
        l = [] 
        for i in y:
           l.append((i.username,i.password))
        if (a,b) in l:
            return redirect("/admin_dashboard")
        else:
            return redirect('/')

@app.route('/success',methods=['GET','POST'])
def success():
    return render_template('success.html')

#==============================User Dashboard=================================
@app.route('/user_dashboard/<id>',methods=['GET','POST'])
def user_dashboard(id):
    categories = Category.query.all()
    return render_template('user_dashboard.html',categories=categories,name=id)


#========================Add a Category======================================
@app.route('/admin_dashboard',methods=['GET','POST'])
def admin_dashboard():
    if request.method == "GET":
        categories = Category.query.all()
        customers = User.query.all()
        return render_template('admin_dashboard.html',categories=categories,customers=customers)
    elif request.method == "POST":
        a = request.form['nameInput']
        if(a!=''):
            c = Category(name=a)
            db.session.add(c)
            db.session.commit()
            return redirect('/admin_dashboard')
        else:
            return redirect('/admin_dashboard')
        


#===============================upload cstegory img======================================
upload_folder = os.path.join('static', 'uploads')

app.config['UPLOAD'] = upload_folder
@app.route('/admin_dashboard/<name>', methods=['GET', 'POST'])
def upload_file(name):
    if request.method == 'POST':
        file = request.files['img']
        filename = name+".png"
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)
        return redirect ('/admin_dashboard')
    return redirect ('/admin_dashboard')

#===============================upload product img======================================
@app.route('/Products_of_Category/<int:id>/<name>', methods=['GET', 'POST'])
def upload_file_product(id,name):
    if request.method == 'POST':
        file = request.files['img']
        filename = name+".png"
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)
        return redirect(url_for('view_product',id = id))
    return redirect(url_for('view_product',id = id))


#========================Edit Category=============================
@app.route("/edit_category/<int:cid>",methods=["GET","POST"])
def edit_category(cid):
    if request.method == "GET":
        categories = Category.query.all()
        customers = User.query.all()
        return render_template('edit_category.html',categories=categories,customers=customers,a=cid-1)
    elif request.method == "POST":
        a = request.form['nameInput']
        if(a!=''):
            Category.query.filter_by(id = cid).update({'name':a})
            db.session.commit()
            return redirect('/admin_dashboard')
        else:
            return redirect('/admin_dashboard')





#===================Delete a Category======================================
@app.route("/delete_category/<int:id>",methods=["GET","POST"])
def delete_category(id):
    C1 = Category.query.get(id)
    p1 = C1.product_relation 
    for i in p1:
        db.session.delete(i)
    db.session.delete(C1)
    db.session.commit()
    

    return redirect('/admin_dashboard')

#=======================View Products for Admin Dashboard===================
@app.route("/Products_of_Category/<int:id>",methods=["GET","POST"])
def view_product(id):
    c = Category.query.get(id)
    products = c.product_relation
    return render_template('Products_of_Category.html',products=products,c=c)

#=======================Add Product========================================

@app.route('/add_product/<int:id>',methods=['GET','POST'])
def add_product(id):
    if request.method == "GET":
        return render_template('add_product.html')
    elif request.method == "POST":
        a = request.form['name']
        b = request.form['unit']
        c1 = request.form['quantity']
        d = request.form['manufacture_date']
        e = request.form['expiry_date']
        r = request.form['rate']
        c = id
        product = Product(name=a,unit=b,rate=r,quantity=c1,manufacture_date=d,expiry_date=e,category_id=c)
        db.session.add(product)
        db.session.commit()
        p = Product.query.filter_by(name = a,rate=r,quantity=c1,manufacture_date=d,expiry_date=e,category_id=c).first()
        pid = p.id
        cr = Association.query.filter_by(category_id = c,product_id = pid).first()
        if cr is None:
             assos = Association(category_id = c,product_id = pid)
             db.session.add(assos)
             db.session.commit()            
        return redirect(url_for('view_product',id = c))
    
#=======================Delete Product========================================
@app.route('/delete_product/<int:c_id>/<int:id>', methods = ['GET', 'POST'])
def delete_product(id,c_id):
    Product.query.filter_by(id = id).delete()
    db.session.commit()
    Association.query.filter_by(product_id = id).delete()
    db.session.commit()
    c_id = c_id
    return redirect(url_for('view_product',id = c_id))

#=======================Edit Product Name========================================
@app.route("/edit_product_name/<int:id>/<int:pid>",methods=["GET","POST"])
def edit_product_name(id,pid):
    if request.method == "GET":
        c = Category.query.get(id)
        products = c.product_relation
        return render_template('edit_product_name.html',products=products,c=c,a=pid-1)
    elif request.method == "POST":
        a = request.form['nameInput']
        if(a!=''):
            Product.query.filter_by(id = pid).update({'name':a})
            db.session.commit()
            return redirect(url_for('view_product',id = id))
        else:
            return redirect(url_for('view_product',id = id))
        
#=======================Edit Product Unit========================================
@app.route("/edit_product_unit/<int:id>/<int:pid>",methods=["GET","POST"])
def edit_product_unit(id,pid):
    if request.method == "GET":
        c = Category.query.get(id)
        products = c.product_relation
        return render_template('edit_product_unit.html',products=products,c=c,a=pid-1)
    elif request.method == "POST":
        a = request.form['unit']
        if(a!=''):
            Product.query.filter_by(id = pid).update({'unit':a})
            db.session.commit()
            return redirect(url_for('view_product',id = id))
        else:
            return redirect(url_for('view_product',id = id))
        
#=======================Edit Product Rate========================================

@app.route("/edit_product_rate/<int:id>/<int:pid>",methods=["GET","POST"])
def edit_product_rate(id,pid):
    if request.method == "GET":
        c = Category.query.get(id)
        products = c.product_relation
        return render_template('edit_product_rate.html',products=products,c=c,a=pid-1)
    elif request.method == "POST":
        a = request.form['nameInput']
        if(int(a)>=0 and a!=''):
            Product.query.filter_by(id = pid).update({'rate':int(a)})
            db.session.commit()
            return redirect(url_for('view_product',id = id))
        else:
            return redirect(url_for('view_product',id = id))
        
#=======================Edit Product Quantity========================================
@app.route("/edit_product_qty/<int:id>/<int:pid>",methods=["GET","POST"])
def edit_product_qty(id,pid):
    if request.method == "GET":
        c = Category.query.get(id)
        products = c.product_relation
        return render_template('edit_product_qty.html',products=products,c=c,a=pid-1)
    elif request.method == "POST":
        a = request.form['nameInput']
        if(int(a)>=0 or a!=''):
            Product.query.filter_by(id = pid).update({'quantity':int(a)})
            db.session.commit()
            return redirect(url_for('view_product',id = id))
        else:
            return redirect(url_for('view_product',id = id))
        
#=======================Edit Product Manufacture Date========================================
@app.route("/edit_product_md/<int:id>/<int:pid>",methods=["GET","POST"])
def edit_product_md(id,pid):
    if request.method == "GET":
        c = Category.query.get(id)
        products = c.product_relation
        return render_template('edit_product_md.html',products=products,c=c,a=pid-1)
    elif request.method == "POST":
        a = request.form['nameInput']
        if(a!=''):
            Product.query.filter_by(id = pid).update({'manufacture_date':a})
            db.session.commit()
            return redirect(url_for('view_product',id = id))
        else:
            return redirect(url_for('view_product',id = id))
        
#=======================Edit Product Expiry Date========================================
@app.route("/edit_product_ed/<int:id>/<int:pid>",methods=["GET","POST"])
def edit_product_ed(id,pid):
    if request.method == "GET":
        c = Category.query.get(id)
        products = c.product_relation
        return render_template('edit_product_ed.html',products=products,c=c,a=pid-1)
    elif request.method == "POST":
        a = request.form['nameInput']
        if(a!=''):
            Product.query.filter_by(id = pid).update({'expiry_date':a})
            db.session.commit()
            return redirect(url_for('view_product',id = id))
        else:
            return redirect(url_for('view_product',id = id))


#=======================View Products for User Dashboard===================
@app.route("/view_products/<name>/<int:id>",methods=["GET","POST"])
def view_products(name,id):
    c = Category.query.get(id)
    products = c.product_relation
    return render_template('view_products.html',products=products,c=c,name=name)

#=======================Add Product to Cart=========================================

@app.route("/add_to_cart/<name>/<int:c_id>/<int:id>",methods=["GET","POST"])
def add_to_cart(name,c_id,id):
    if request.method == "POST":
        p = Product.query.filter_by(id=id).first()
        p_unit = p.unit
        p_name = p.name
        p_rate = p.rate
        a = request.form['Qty']

        if(int(p.quantity)>=int(a)):
            cart = Cart(name=name,product_id=id,product_name=p_name,req_quantity=a,product_rate=p_rate,product_unit=p_unit)
            db.session.add(cart)
            db.session.commit()
            return redirect(url_for('view_products',name=name,id = c_id))
        else:
            return redirect(url_for('view_products',name=name,id = c_id))
        



#=======================View User Cart=========================================
@app.route('/view_cart/<name>',methods=['GET','POST'])
def view_cart(name):
    p = Cart.query.filter_by(name=name).all()
    gt = 0
    for i in p:
        a = i.product_rate * i.req_quantity
        gt+=a
    return render_template('view_cart.html',products=p,name=name,gt=gt)

#=======================Delete Product in Cart========================================
@app.route('/delete_product_cart/<name>/<int:id>',methods=['GET','POST'])
def delete_product_cart(name,id):
    Cart.query.filter_by(id = id).delete()
    db.session.commit()
    return redirect(url_for('view_cart',name=name))


#=======================Add Product to Bought=========================================

@app.route("/Buy/<name>",methods=["GET","POST"])
def add_to_bought(name):
    products_bought = Cart.query.filter_by(name=name).all()
    for p in products_bought:
        pid = p.product_id
        pname = p.product_name
        qty = p.req_quantity
        prate = p.product_rate
        punit = p.product_unit
        bought = Bought(name=name,product_id=pid,product_name=pname,req_quantity=qty,product_rate=prate,product_unit=punit)
        db.session.add(bought)
        db.session.commit()
        p = Product.query.filter_by(id = pid).first()
        p1 = int(p.quantity) - int(qty)
        Product.query.filter_by(id = pid).update({'quantity':p1})
        db.session.commit()
    
    Cart.query.filter_by(name=name).delete()
    db.session.commit()
    
    return render_template("order_successful.html",name=name)


#=======================View User Account=========================================
@app.route('/my_account/<name>',methods=['GET','POST'])
def my_account(name):
    p = Bought.query.filter_by(name=name).all()
    gt = 0
    for i in p:
        a = i.product_rate * i.req_quantity
        gt+=a
    return render_template('my_account.html',products=p,name=name,gt=gt)

#=======================View Orders in Admin Dashboard=========================================
@app.route('/view_orders/<name>',methods=['GET','POST'])
def view_orders(name):
    p = Bought.query.filter_by(name=name).all()
    gt = 0
    for i in p:
        a = i.product_rate * i.req_quantity
        gt+=a
    return render_template('view_orders.html',products=p,name=name,gt=gt)

@app.route('/unsuccessful',methods=['GET','POST'])
def unsuccessful():
    return render_template('unsuccessful.html')


if __name__ == "__main__":
    app.run(debug=True)