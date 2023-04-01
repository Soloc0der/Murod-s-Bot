import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            Name varchar(255) NOT NULL,
            email varchar(255),
            language varchar(3),
            phone_number varchar(15),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    def create_table_cats(self):
        sql = """
        CREATE TABLE Category (
            id INTEGER PRIMARY KEY,
            name varchar(255) NOT NULL UNIQUE,
            desc TEXT,
            image TEXT NOT NULL
            );"""
        self.execute(sql, commit=True)

    def create_table_products(self):
        sql = """
        CREATE TABLE Product (
            id INTEGER PRIMARY KEY,
            name varchar(255) NOT NULL UNIQUE,
            desc TEXT NOT NULL,
            image TEXT NOT NULL,
            price REAL NOT NULL,
            cat_id INTEGER NOT NULL
            );"""
        self.execute(sql, commit=True)

    def create_table_cart(self):
        sql = """
        CREATE TABLE Cart (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL UNIQUE
            );"""
        self.execute(sql, commit=True)

    def create_table_cart_items(self):
        sql = """
        CREATE TABLE CartItem (
            id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            cart_id INTEGER NOT NULL
            );"""
        self.execute(sql, commit=True)

    def create_table_order(self):
        sql = """
        CREATE TABLE Orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            total_price REAL NOT NULL,
            lat REAL,
            lon REAL
            );"""
        self.execute(sql, commit=True)
   

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, name: str, email: str = None, language: str = 'uz',phone_number=None):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(id, Name, email, language,phone_number) VALUES(?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, email, language,phone_number), commit=True)

    def add_user_cart(self, user_id: int):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Cart(user_id) VALUES(?)
        """
        self.execute(sql, parameters=(user_id,), commit=True)

    def add_order(self, user_id: int, total_price: float, lat: float, lon: float):
        sql = """
        INSERT INTO Orders(user_id, total_price,lat,lon) VALUES(?,?,?,?)
        """
        self.execute(sql, parameters=(user_id, total_price,lat,lon), commit=True)



    def add_cart_item(self, product_id: int, quantity: int, cart_id: int): 
        sql = """
        INSERT INTO CartItem(product_id, quantity, cart_id) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(product_id, quantity, cart_id), commit=True)

    def check_product_exist(self, product_id: int, cart_id: int):
        sql = """SELECT * FROM CartItem WHERE product_id =? AND cart_id=?;"""
        return self.execute(sql, parameters=(product_id,cart_id), fetchone=True)

    def cart_product_update(self, product_id: int, quantity: int, cart_id: int):
        sql = """UPDATE CartItem SET quantity=? WHERE product_id=? AND cart_id=?;"""
        self.execute(sql, parameters=(quantity,product_id, cart_id), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def get_all_items(self, **kwargs):
        sql = "SELECT product_id, quantity FROM CartItem WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_all_cats(self):
        sql = """
        SELECT * FROM Category;
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_cart(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Cart WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def get_category(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Category WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_all_products(self, **kwargs):
        sql = "SELECT * FROM Product WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def get_product_data(self, **kwargs):
        sql = "SELECT * FROM Product WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


    def delete_user_cart_items(self, cart_id):
        sql = "DELETE FROM CartItem WHERE cart_id=?;"
        self.execute(sql=sql, parameters=(cart_id,), commit=True)


    def  delete_product_user_cart(self, product_id, cart_id):
         sql = "DELETE FROM CartItem WHERE cart_id=? AND product_id=?;"
         self.execute(sql=sql, parameters=(cart_id, product_id), commit=True)


def logger(statement):
    print(f"""
_____________________________________________________
Executing:
{statement}
_____________________________________________________
""")
