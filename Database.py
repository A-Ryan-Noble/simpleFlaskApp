import MySQLdb
from entities.Users import User
from entities.Products import Product
from faker import Faker


def drop_tables():
    db = MySQLdb.connect(host="localhost", user="root", password="pass", database="flaskDb")
    cursor = db.cursor()

    cursor.execute("DROP TABLE IF EXISTS products")  # Drop table if it already exist
    cursor.execute("DROP TABLE IF EXISTS users")  # Drop table if it already exist

    # Disconnect from server
    cursor.close()
    db.close()


def open_db_connection():
    db = MySQLdb.connect(host="localhost", user="root", password="pass", database="flaskDb")  # Open database connection
    cursor = db.cursor()
    return db, cursor


def create_tables():
    db = MySQLdb.connect(host="localhost", user="root", password="pass", database="flaskDb")  # Open database connection
    cursor = db.cursor()  # Prepare a cursor object

    # Users table creation
    sql = """CREATE TABLE IF NOT EXISTS users(
                 Id integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
                 Name varchar(255) NOT NULL,
                 Password varchar(255) NOT NULL,
                 Role varchar(5) NOT NULL,
                 UNIQUE KEY `username_UNIQUE` (`Name`))"""

    sql2 = """CREATE TABLE IF NOT EXISTS products(
                 Id integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
                 Name varchar(255) NOT NULL,
                 Price DECIMAL(19 , 2) UNSIGNED zerofill,
                 Img varchar(255) NOT NULL,
                 OwnedBy varchar(255),
                 FOREIGN KEY (OwnedBy) REFERENCES users(Name),
                 UNIQUE KEY `product_name_UNIQUE` (`Name`))"""

    cursor.execute(sql)
    cursor.execute(sql2)

    return db, cursor


def insert_user(user):
    db, cursor = create_tables()

    details = user.get_details()

    sql = "INSERT INTO users(name,password,role) VALUES ('%s', '%s', '%s')" % (details[0], details[1], details[2])

    try:
        cursor.execute(sql)  # Execute the SQL command

        db.commit()  # Commit your changes in the database

    except:

        db.rollback()  # Rollback in case there is any error

    # Disconnect from server
    cursor.close()
    db.close()


def user_exists(name):
    db, cursor = create_tables()

    sql = "SELECT count(name) FROM users WHERE name = ('%s')" % name

    try:
        cursor.execute(sql)  # Execute the SQL command

        is_name_there = cursor.fetchone()[0]

        # Disconnect from server
        cursor.close()
        db.close()

        if is_name_there == 0:
            return False;
        else:
            return True

    except:
        db.rollback()  # Rollback in case there is any error

        # Disconnect from server
        cursor.close()
        db.close()


def get_user_id_by_name(name):
    db, cursor = create_tables()

    sql = "SELECT id FROM users WHERE name = ('%s')" % name

    try:
        cursor.execute(sql)  # Execute the SQL command

        user_id = cursor.fetchone()[0]

        # Disconnect from server
        cursor.close()
        db.close()

        print(f"id is: {user_id}")
        return user_id

    except:
        db.rollback()  # Rollback in case there is any error

        # Disconnect from server
        cursor.close()
        db.close()


def update_name(old_name, new_name):
    db, cursor = create_tables()

    sql = "UPDATE users SET name = ('%s') WHERE name = ('%s')" % (new_name, old_name)

    try:
        cursor.execute(sql)
        db.commit()

    except:
        db.rollback()  # Rollback in case there is any error

    # Disconnect from server
    cursor.close()
    db.close()


def update_password(name, password):
    db, cursor = create_tables()

    sql = "UPDATE users SET password = ('%s') WHERE name = ('%s')" % (password, name)

    try:
        cursor.execute(sql)  # Execute the SQL command

        db.commit()  # Commit your changes in the database

    except:
        db.rollback()  # Rollback in case there is any error

        # Disconnect from server
        cursor.close()
        db.close()


def update_access(name, role):
    db, cursor = create_tables()

    sql = "UPDATE users SET role = ('%s') WHERE name = ('%s')" % (role, name)

    try:
        cursor.execute(sql)  # Execute the SQL command

        db.commit()  # Commit your changes in the database

    except:
        db.rollback()  # Rollback in case there is any error

    # Disconnect from server
    cursor.close()
    db.close()


def delete_user(name):
    db, cursor = create_tables()

    sql = "DELETE FROM users WHERE name = '%s'" % name

    try:
        cursor.execute(sql)  # Execute the SQL command
        db.commit()  # Commit your changes in the database

    except:
        db.rollback()  # Rollback in case there is any error

    # Disconnect from server
    cursor.close()
    db.close()


def get_users():
    db, cursor = create_tables()

    sql = "SELECT * FROM users"

    try:
        cursor.execute(sql)  # Execute the SQL command

        details = cursor.fetchall()

        # Disconnect from server
        cursor.close()
        db.close()

        return details

    except:
        db.rollback()  # Rollback in case there is any error

        # Disconnect from server
        cursor.close()
        db.close()


def user_details_by_name(name):
    db, cursor = create_tables()

    sql = "SELECT name,password,role FROM users WHERE name = ('%s')" % name
    try:
        cursor.execute(sql)  # Execute the SQL command

        details = cursor.fetchone()

        # Disconnect from server
        cursor.close()
        db.close()

        return details

    except:
        db.rollback()  # Rollback in case there is any error

        # Disconnect from server
        cursor.close()
        db.close()


def update_user(og_name, new_name, password, role):
    update_access(og_name, role)
    update_password(og_name, password)

    # Remove user as owner of the product(s) returning the title of each product
    product_names = remove_owner(og_name)

    update_name(og_name, new_name)
    update_owner(new_name, product_names)


def get_name_of_users():
    db, cursor = create_tables()

    # Names returned will be in ascending order I.e. A->B->C...
    sql = "select name from users order by Name ASC"

    try:
        cursor.execute(sql)  # Execute the SQL command

        all_users = cursor.fetchall()

        names = []

        # list of names returned is made in the following manner:
        # (('admin',), ...) to ('admin',....)
        for x in range(0, len(all_users)):
            names.append(all_users[x][0])

        # Disconnect from server
        cursor.close()
        db.close()

        return names

    except:
        db.rollback()  # Rollback in case there is any error

    # Disconnect from server
    cursor.close()
    db.close()


def insert_product(product):
    db, cursor = create_tables()

    details = product.get_details()

    sql = "INSERT INTO products(Name, price, img, OwnedBy) VALUES ('%s', '%s', '%s', '%s')" % \
          (details[0], details[1], details[2], details[3])

    try:
        cursor.execute(sql)  # Execute the SQL command

        db.commit()  # Commit your changes in the database

    except:

        db.rollback()  # Rollback in case there is any error

    # Disconnect from server
    cursor.close()
    db.close()


def get_products():
    db, cursor = create_tables()

    sql = "select * from products order by Name ASC"

    try:
        cursor.execute(sql)  # Execute the SQL command

        details = cursor.fetchall()

        # Disconnect from server
        cursor.close()
        db.close()

        return details

    except:
        db.rollback()  # Rollback in case there is any error

        # Disconnect from server
        cursor.close()
        db.close()


def get_names_of_product():
    db, cursor = create_tables()

    # Names returned will be in ascending order I.e. A->B->C...
    sql = "select name from products order by Name ASC"

    try:
        cursor.execute(sql)  # Execute the SQL command

        all_users = cursor.fetchall()

        names = []

        # list of names returned is made in the following manner:
        # (('admin',), ...) to ('admin',....)
        for x in range(0, len(all_users)):
            names.append(all_users[x][0])

        # Disconnect from server
        cursor.close()
        db.close()

        return names

    except:
        db.rollback()  # Rollback in case there is any error

    # Disconnect from server
    cursor.close()
    db.close()


def get_product_name(name):
    db, cursor = create_tables()

    # Names returned will be in ascending order I.e. A->B->C...
    sql = "select name from products order by Name WHERE name = ('%s')" % name

    try:
        cursor.execute(sql)  # Execute the SQL command

        all_products = cursor.fetchall()

        names = []

        # list of names returned is made in the following manner:
        # (('admin',), ...) to ('admin',....)
        for x in range(0, len(all_products)):
            names.append(all_products[x][0])

        # Disconnect from server
        cursor.close()
        db.close()

        return names

    except:
        db.rollback()  # Rollback in case there is any error

    # Disconnect from server
    cursor.close()
    db.close()


def product_details_by_name(name):
    db, cursor = create_tables()

    sql = "SELECT name,price,img,ownedBy FROM products WHERE name = ('%s')" % name

    try:
        cursor.execute(sql)  # Execute the SQL command

        details = cursor.fetchone()

        # Disconnect from server
        cursor.close()
        db.close()

        return details

    except:
        db.rollback()  # Rollback in case there is any error

        # Disconnect from server
        cursor.close()
        db.close()


def product_details_by_price():
    db, cursor = create_tables()

    sql = "select * from products order by PRICE ASC"

    try:
        cursor.execute(sql)  # Execute the SQL command

        details = cursor.fetchall()

        # Disconnect from server
        cursor.close()
        db.close()

        return details

    except:
        db.rollback()  # Rollback in case there is any error

        # Disconnect from server
        cursor.close()
        db.close()


def get_product_images_by_name(name):
    db, cursor = create_tables()

    sql = "select img from products WHERE name = ('%s')" % name

    try:
        cursor.execute(sql)  # Execute the SQL command

        all_products = cursor.fetchall()

        images = []

        # list of names returned is made in the following manner:
        # (('admin',), ...) to ('admin',....)
        for x in range(0, len(all_products)):
            images.append(all_products[x][0])

        # Disconnect from server
        cursor.close()
        db.close()

        return images

    except:
        db.rollback()  # Rollback in case there is any error

    # Disconnect from server
    cursor.close()
    db.close()


def get_product_owner_by_name(name):
    db, cursor = create_tables()

    sql = "SELECT ownedBy FROM products WHERE name = ('%s')" % name

    try:
        cursor.execute(sql)  # Execute the SQL command

        owner = cursor.fetchone()[0]

        # Disconnect from server
        cursor.close()
        db.close()

        return owner

    except:
        db.rollback()  # Rollback in case there is any error

        # Disconnect from server
        cursor.close()
        db.close()


def update_product_name(old_name, new_name):
    db, cursor = create_tables()

    sql = "UPDATE products SET name = ('%s') WHERE name = ('%s')" % (new_name, old_name)

    try:
        cursor.execute(sql)  # Execute the SQL command
        db.commit()  # Commit your changes in the database

    except:
        db.rollback()  # Rollback in case there is any error

    # Disconnect from server
    cursor.close()
    db.close()


def remove_owner(og_name):
    db, cursor = create_tables()

    # Get name(s) of of products that the user to be changed owns
    sql = "Select name from products WHERE OwnedBy = ('%s')" % og_name

    try:
        cursor.execute(sql)  # Execute the SQL command

        # Gets the only the products names returned from the database
        names = []

        for item in cursor.fetchall():
            names.append(item[0])

        # Remove the name of the user from the products
        sql2 = "UPDATE products SET OwnedBy = NULL WHERE OwnedBy = ('%s')" % og_name

        cursor.execute(sql2)

        db.commit()  # Commit your changes in the database

        cursor.close()
        db.close()

        return names

    except:
        db.rollback()  # Rollback in case there is any error

        # Disconnect from server
        cursor.close()
        db.close()


def update_owner(new_owner, product_names):
    db, cursor = create_tables()

    for product_name in product_names:
        sql = "UPDATE products SET OwnedBy = ('%s') WHERE name = ('%s')" % (new_owner, product_name)

        try:
            cursor.execute(sql)  # Execute the SQL command

            db.commit()  # Commit your changes in the database

        except:
            db.rollback()  # Rollback in case there is any error

    # Disconnect from server
    cursor.close()
    db.close()


def update_price(price, name):
    db, cursor = create_tables()

    sql = "UPDATE products SET Price = ('%s') WHERE Name = ('%s')" % (price, name)

    try:
        cursor.execute(sql)

        db.commit()

    except:
        db.rollback()  # Rollback in case there is any error

    # Disconnect from server
    cursor.close()
    db.close()


def update_file(filename, name):
    db, cursor = create_tables()

    sql = "UPDATE products SET Img = ('%s') WHERE Name = ('%s')" % (filename, name)

    try:
        cursor.execute(sql)

        db.commit()

    except:
        db.rollback()  # Rollback in case there is any error

    # Disconnect from server
    cursor.close()
    db.close()


def update_product(old_name, product):
    details = product.get_details()

    update_owner(details[3], old_name)

    update_file(details[2], old_name)

    update_price(details[1], old_name)

    update_product_name(old_name, details[0])


def delete_product(name):
    db, cursor = create_tables()

    sql = "DELETE FROM products WHERE name = '%s'" % name

    try:
        cursor.execute(sql)  # Execute the SQL command
        db.commit()  # Commit your changes in the database

    except:
        db.rollback()  # Rollback in case there is any error

    # Disconnect from server
    cursor.close()
    db.close()


def products_owned_by_user(user_name):
    db, cursor = create_tables()

    sql = "Select name,price,img,ownedBy from products WHERE OwnedBy = ('%s')" % user_name

    try:
        cursor.execute(sql)  # Execute the SQL command

        # Gets the only the products names returned from the database
        products = []

        for item in cursor.fetchall():
            products.append(item)

        cursor.close()
        db.close()

        return products

    except:
        db.rollback()  # Rollback in case there is any error

        # Disconnect from server
        cursor.close()
        db.close()


def users_total_cost(user_name):
    db, cursor = create_tables()

    sql = "Select sum(price) from products WHERE OwnedBy = ('%s')" % user_name

    cursor.execute(sql)  # Execute the SQL command

    total = cursor.fetchone()[0]

    # Disconnect from server
    cursor.close()
    db.close()

    return total


def unique_users_list():
    db, cursor = create_tables()

    sql = "select DISTINCT OwnedBy from products"

    cursor.execute(sql)

    users_list = []

    for user in cursor.fetchall():
        users_list.append(user[0])

    cursor.close()
    db.close()

    return users_list


def name_of_products_owned_by_user(user_name):
    db, cursor = create_tables()

    sql = "Select name from products WHERE OwnedBy = ('%s')" % user_name

    try:
        cursor.execute(sql)  # Execute the SQL command

        # Gets the only the products names returned from the database
        products = []

        for item in cursor.fetchall():
            products.append(item[0])

        cursor.close()
        db.close()

        return products

    except:
        db.rollback()  # Rollback in case there is any error

        # Disconnect from server
        cursor.close()
        db.close()


def price_of_product_by_name_and_owner(owner, product_name):
    db, cursor = create_tables()

    sql = "Select price from products WHERE OwnedBy = ('%s') and Name = ('%s')" % (owner, product_name)

    try:
        cursor.execute(sql)  # Execute the SQL command

        price = cursor.fetchone()[0]

        cursor.close()
        db.close()

        return price

    except:
        db.rollback()  # Rollback in case there is any error

        # Disconnect from server
        cursor.close()
        db.close()


# Generate 5 random users and insert into database
def faker_db():
    fake = Faker(["en_ie", "en_us", "en_GB"])

    images = ["Bookshelf.jpg", "Apple.png", "MinimalistBookDesign.jpg", "Car.png",
            "Fruit.jpg", "Chair.jpg", "Football.jpg", "Fridge.jpg", "BlankProfile.png"]

    for x in range(0, 8):
        name = fake.first_name()
        words_passwords = fake.words(1)[0]

        u = User(name, words_passwords)

        if x % 2:
            u.make_user_admin()

        insert_user(u)

        product_name = fake.words(2)[0]
        price = fake.random_int(0, 1000)

        img = images[fake.random_int(0, len(images)-1)]

        p = Product(product_name, price, img, name)

        insert_product(p)

# Function that sets up the database
def refresh_db():
    drop_tables()
    create_tables()

    user1 = User('user', 'pass')
    user2 = User('admin', 'pass', 'admin')
    user3 = User('ryan1', 'ryan1')
    user4 = User('ryan2', 'ryan2')
    user4.make_user_admin()
    user5 = User('ryan', 'ryan')

    insert_user(user1)
    insert_user(user2)
    insert_user(user3)
    insert_user(user4)
    insert_user(user5)

    product1 = Product("Bookshelf", 56.99, "Bookshelf.jpg", user1.get_name())
    product2 = Product("Apple", 3.68, "Apple.png", user2.get_name())
    product3 = Product("Book", 45.4, "MinimalistBookDesign.jpg", user3.get_name())
    product4 = Product("Car", 1243.30, "Car.png", user4.get_name())
    product5 = Product("Fruit", 1, "Fruit.jpg", user5.get_name())
    product6 = Product("Chair", 120.57, "Chair.jpg", user5.get_name())
    product7 = Product("Football", 20, "Football.jpg", user3.get_name())
    product8 = Product("Fridge", 677, "Fridge.jpg", user3.get_name())

    insert_product(product1)
    insert_product(product2)
    insert_product(product3)
    insert_product(product4)
    insert_product(product5)
    insert_product(product5)
    insert_product(product6)
    insert_product(product7)
    insert_product(product8)

    faker_db()
