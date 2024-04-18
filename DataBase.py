import sqlite3

connection = sqlite3.connect('cusineCart.db',check_same_thread=False)
cursor = connection.cursor()

def create_tables():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Email TEXT,
                        Password TEXT,
                        Name TEXT,
                        Address TEXT,
                        Phone TEXT,
                        RegistrationDate TEXT
                    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Restaurants (
                        RestaurantID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Email TEXT,
                        Name TEXT,
                        Password TEXT,
                        Description TEXT,
                        Address TEXT,
                        Phone TEXT,
                        Website TEXT,
                        OpeningHours TEXT,
                        RegistrationDate TEXT
                    );''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Menus (
                        MenuID INTEGER PRIMARY KEY AUTOINCREMENT,
                        RestaurantID INTEGER,
                        ItemName TEXT,
                        Description TEXT,
                        Price REAL,
                        Category TEXT,
                        ImagePNG TEXT,
                        ImageJPG TEXT,
                        FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID)
                    );''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Promotions (
                        PromotionID INTEGER PRIMARY KEY AUTOINCREMENT,
                        RestaurantID INTEGER,
                        PromotionName TEXT,
                        MenuID INTEGER,
                        Description TEXT,
                        Discount REAL,
                        StartDate TEXT,
                        EndDate TEXT,
                        FOREIGN KEY (RestaurantID) REFERENCES Restaurants (RestaurantID),
                        FOREIGN KEY (MenuID) REFERENCES Menus (MenuID)
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

def EmailCheck(email):
    try:
        cursor.execute('''SELECT * FROM Users Where email=?;''',[email])
        user_data = cursor.fetchone()
        if user_data:
            return 'User'

        cursor.execute('''SELECT * FROM Restaurants Where email=?;;''',[email])
        user_data = cursor.fetchone()
        if user_data:
            return 'Restaurant'

        return 'No data found with this email and password'
    except Exception as e:
        return f'Error: {str(e)}'



def get_menu_data(limit=100):
    try:
        cursor.execute('''SELECT ItemName, Description, Price, ImagePNG ,Category  FROM Menus LIMIT ?''',[limit])
        return cursor.fetchall()
    except sqlite3.Error as e:
        print("Error fetching data from database:", e)
        print('here')
        return []


def get_active_promotions(current_date,limit=100):
    try:
        cursor.execute("""SELECT p.PromotionName, m.Price, p.Discount, m.ImageJPG FROM Promotions p JOIN Menus m ON p.MenuID = m.MenuID
                        WHERE p.StartDate <= ? AND p.EndDate >= ? Limit ?""", [current_date, current_date,limit])
        rows = cursor.fetchall()
        promotions_data = []
        for row in rows:
            promotion_name, price, discount, image = row
            discounted_price = price * (1 - discount / 100)
            promotions_data.append({'PromotionName': promotion_name,'Price': price,'Discount': discount,'Image': image,'DiscountedPrice': discounted_price})
        return promotions_data
    except sqlite3.Error as e:
        print("Error fetching data from database:", e)
        print('here2')
        
        return []


def close_connection():
    connection.close()
