from flask import Flask, redirect, session, flash
from flask.globals import request
from flask.templating import render_template
import Database
from Config import Config
from entities.Users import User
from entities.Products import Product
from forms import NewProductForm
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm
from forms.UpdateForm import UpdateForm
from forms.NewProductForm import NewProductForm
from forms.UpdateProductForm import UpdateProductForm
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config.from_object(Config)
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH
app.config['UPLOAD_EXTENSIONS'] = Config.UPLOAD_EXTENSIONS
app.config['UPLOAD_PATH'] = Config.IMAGE_UPLOAD_FOLDER


@app.route('/')
def index():
    if 'username' not in session:
        return render_template('index.html', title="Home")

    name = session.get('username')

    user_details = Database.user_details_by_name(name)
    user_products = Database.products_owned_by_user(name)

    info = make_info_message(name, user_products)
    return render_template('welcome.html', title="Hello", user=user_details, products=user_products, messages=info)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(request.referrer)

    form = LoginForm()

    if form.validate_on_submit():

        name = form.username.data

        exists = Database.user_exists(name)

        if exists:

            details = Database.user_details_by_name(name)

            u = User(details[0], details[1], details[2])

            # if user is already logged in get their name and if they have admin access, otherwise add it
            if 'username' in session:
                session['username'] = session.get('username')
                session['access'] = session.get('access')

            else:
                session['username'] = details[0]
                session['access'] = u.is_admin(details[2])

            return redirect('/')

        else:
            flash("User not found!", 'noUser')
            return redirect('/login')

    return render_template('login.html', title="Login", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' not in session:
        return redirect(request.referrer)

    form = RegisterForm()

    if form.validate_on_submit():

        name = form.username.data
        password = form.password.data

        exists = Database.user_exists(name)

        if not exists:
            user = User(name, password)

            if session.get('access'):
                user.make_user_admin()

            Database.insert_user(user)

            return redirect('/')

        else:
            flash("Username already taken!", 'userTakenMsg')
            return redirect('/register')

    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    if 'username' not in session:
        return redirect(request.referrer)

    session.pop('username', None)
    session.pop('access', None)
    return redirect('/')


@app.route('/listUsers')
def list_all_users():
    if 'username' not in session:
        return redirect(request.referrer)

    all_users = Database.get_users()

    return render_template('viewAllUsers.html', title="Viewing Users", users=all_users)


@app.route('/viewOneUser/<string:name>')
def view_one_user(name):
    if 'username' not in session:
        return redirect(request.referrer)

    user = Database.user_details_by_name(name)

    return render_template('viewOneUser.html', title="Viewing User", user=user)


@app.route('/editUser/<string:name>', methods=['GET', 'POST'])
def edit_user(name):
    if 'username' not in session:
        return redirect(request.referrer)

    index_pg = 'http://127.0.0.1:5000/'

    previous_pg = request.referrer

    users = Database.get_name_of_users()

    # If they come from the index page
    if previous_pg == index_pg:
        users = [name]  # Only the logged in user is to be displayed

    form = UpdateForm()

    if form.is_submitted():
        old_name = form.nameToChange.data
        new_name = form.newUsername.data
        new_password = form.newPassword.data

        role = "user"

        # If true is returned then make admin
        if form.newRole.data:
            role = "admin"

        Database.update_user(old_name, new_name, new_password, role)  # User is updated with these changes

        return redirect('/listUsers')

    form.nameToChange.choices = users  # All the available names are made to be possible choices in the form

    form.nameToChange.default = name  # The name of the user in clicked edit button's row is made default

    form.process()  # Processes the change in the default

    return render_template('editUser.html', title="Editing User", form=form)


@app.route('/deleteUser/<string:name>', methods=['GET', 'POST'])
def delete_user(name):
    if 'username' not in session:
        return redirect(request.referrer)

    Database.delete_user(name)

    return redirect('/listUsers')


@app.route('/listProducts')
def list_products():
    all_products = Database.get_products()

    amount = len(all_products)

    msg = "The details for the product, are shown below:"

    if amount > 1:
        msg = f"The details for the {amount} products are shown below:"

    return render_template('viewAllProducts.html', title="Viewing Catalog", products=all_products, message=msg)


@app.route('/newProduct', methods=['GET', 'POST'])
def create_product():
    if 'username' not in session:
        return redirect(request.referrer)

    form = NewProductForm()

    all_users = Database.get_name_of_users()

    form.productOwner.choices = all_users  # All the available names are made to be possible choices in the form

    name = session.get('username')

    form.productOwner.default = name  # The name of the user in clicked edit button's row is made default

    form.process()  # Processes the change in the default

    if request.method == 'POST' and form.is_submitted():
        owner = request.form.get("productOwner")

        product_name = request.form.get("productName")

        # Gets the file name from within the file in form of the posted request
        file = request.files['imageFile']
        filename = secure_filename(file.filename)

        # Saves the file to the designated folder
        file.save(os.path.join(app.config["UPLOAD_PATH"], filename))

        price = request.form.get("productPrice")

        product = Product(product_name, price, filename, owner)

        Database.insert_product(product)

        return redirect('/listProduct')

    return render_template('createProduct.html', title='New Product', form=form)


@app.route('/viewOneProduct/<string:name>')
def view_one_product(name):
    product = Database.product_details_by_name(name)

    return render_template('viewOneProduct.html', title="Viewing Product", product=product)


@app.route('/editProduct/<string:name>', methods=['GET', 'POST'])
def edit_product(name):
    if 'username' not in session:
        return redirect(request.referrer)

    users = Database.get_name_of_users()

    form = UpdateProductForm()

    product = Database.product_details_by_name(name)

    name_product = product[0]
    product_price = product[1]
    product_owner = product[3]

    form.productOwner.choices = users  # All the available names are made to be possible choices in the form

    # Forms default values set
    form.productOwner.default = product_owner
    form.productName.default = name_product
    form.productPrice.default = product_price
    form.imageFile.default = product[2]

    form.process()  # Processes the change in the default

    if request.method == 'POST' and form.is_submitted():

        owner = request.form.get("productOwner")

        product_name = request.form.get("productName")

        # Gets the file name from within the file in form of the posted request
        file = request.files['imageFile']
        filename = secure_filename(file.filename)

        # Saves the file to the designated folder
        file.save(os.path.join(app.config["UPLOAD_PATH"], filename))

        price = request.form.get("productPrice")

        product = Product(product_name, price, filename, owner)

        Database.update_product(name_product, product)

        return redirect('/listProducts')

    return render_template('editProduct.html', title="Editing Product", form=form)


@app.route('/viewProducts/<string:name>')
def view_users_products(name):
    # if name passed ends with the curly bracket then its removed
    if name[len(name) - 1] == "}":
        name = name[0: len(name) - 1]

    user_exists = Database.user_exists(name)

    if not user_exists or 'username' not in session:
        return redirect('/')

    all_products = Database.products_owned_by_user(name)

    info = make_info_message(name, all_products)

    return render_template('viewUserProducts.html', title=(name+"'s Products"), products=all_products, messages=info)


@app.route('/deleteProduct/<string:name>', methods=['GET'])
def delete_product(name):
    if 'username' not in session:
        return redirect(request.referrer)

    Database.delete_product(name)

    return redirect("/listProducts")


@app.route('/viewProducts/productsOverview')
def view_products_overview():
    if 'username' not in session:
        return redirect('/')

    unique_users = Database.unique_users_list()

    details = []

    for user in unique_users:
        users_products = Database.name_of_products_owned_by_user(user)

        products_prices = []

        total = 0

        for users_product in users_products:
            price = Database.price_of_product_by_name_and_owner(user, users_product)
            products_prices.append(price)

            total += price

        details.append([user, users_products, products_prices, total])

    return render_template('productsOverview.html', title="Overview of Products", items=details)


@app.route('/resetDatabase', methods=['GET', 'POST'])
def refresh_db():
    if ('username' not in session) and ('access' not in session):
        return redirect(request.referrer)

    Database.drop_tables()
    Database.create_tables()
    Database.refresh_db()

    session.pop('username', None)
    session.pop('access', None)
    return redirect('/')


def make_info_message(name, all_products):
    amount = len(all_products)

    msg = f"The details for {name}'s product, are shown below:"

    total = Database.users_total_cost(name)

    msg2 = f"Product total comes to €{total}"

    info = [msg, msg2]

    if amount > 1:
        msg = f"The details for {name}'s {amount} products are shown below:"
        msg2 = f"Products total comes to €{total}"
        info = [msg, msg2]

    return info


# Run the application
if __name__ == "__main__":
    app.run(debug=True)
