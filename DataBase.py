import sqlite3

connection = sqlite3.connect('cusineCart.db',check_same_thread=False)
cursor = connection.cursor()

def create_tables():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        Email TEXT PRIMARY KEY,
                        Password TEXT,
                        Name TEXT,
                        Address TEXT,
                        Phone TEXT,
                        RegistrationDate TEXT
                    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Restaurants (
                        Email TEXT PRIMARY KEY,
                        Name TEXT,
                        Password TEXT,
                        Description TEXT,
                        Address TEXT,
                        Phone TEXT,
                        Website TEXT,
                        OpeningHours TEXT,
                        RegistrationDate TEXT
                    );''')



def insert_user(email, password, name=None, address=None, phone=None, registration_date=None):
    try:
        cursor.execute('''INSERT INTO Users (Email, Password, Name, Address, Phone, RegistrationDate)
                          VALUES (?, ?, ?, ?, ?, ?);''',
                       [email, password, name, address, phone, registration_date])
        connection.commit()
        return ''
    except Exception as e:
        return f'Error: {str(e)}'

def insert_restaurants(email, password, name=None, address=None, phone=None, registration_date=None):
    try:
        cursor.execute('''INSERT INTO Restaurants (Email, Password, Name, Address, Phone, RegistrationDate)
                      VALUES (?, ?, ?, ?, ?, ?);''',
                   [email, password, name, address, phone, registration_date])
        connection.commit()
        return ''
    except Exception as e:
        return f'Error: {str(e)}'

def get_all_users():
    cursor.execute('''SELECT * FROM Users;''')
    return cursor.fetchall()

def get_all_restaurants():
    cursor.execute('''SELECT * FROM Restaurants;''' )
    return cursor.fetchall()



def email_exists(email):
    cursor.execute("SELECT * FROM Users WHERE Email=?;", [email])
    user_data = cursor.fetchone()
    
    
    if user_data:
        return True

    cursor.execute("SELECT * FROM Restaurants WHERE Email=?;", [email])
    restaurant_data = cursor.fetchone()
    if restaurant_data:
        return True

    return False


def login_check(email,password):
    if email == None or password == None:
        return 'Enter Values'
    try:
        cursor.execute('''SELECT * FROM Users Where email=? AND password =?;''',[email,password])
        user_data = cursor.fetchone()
        if user_data:
            return 'User'

        cursor.execute('''SELECT * FROM Restaurants Where email=? AND password =?;''',[email,password])
        user_data = cursor.fetchone()
        if user_data:
            return 'Restaurant'

        return 'No data found with this email and password'
    except Exception as e:
        return f'Error: {str(e)}'


def close_connection():
    connection.close()
