import sqlite3

connection = sqlite3.connect('cusineCart.db',check_same_thread=False)
cursor = connection.cursor()

def create_tables():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Customers (
                        CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Email TEXT,
                        Password TEXT,
                        Name TEXT,
                        Address TEXT,
                        Phone TEXT,
                        RegistrationDate TEXT,
                        Blocked INTEGER DEFAULT 0,
                        BlockedByAdmin INTEGER DEFAULT NULL,
                        FOREIGN KEY (BlockedByAdmin) REFERENCES Admin(AdminID)
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
                        RegistrationDate TEXT,
                        Blocked INTEGER DEFAULT 0,
                        BlockedByAdmin INTEGER DEFAULT NULL,
                        FOREIGN KEY (BlockedByAdmin) REFERENCES Admin(AdminID)
                    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Favourites (
                        FavouriteID INTEGER PRIMARY KEY AUTOINCREMENT,
                        UserID INTEGER,
                        MenuID INTEGER,
                        FOREIGN KEY (UserID) REFERENCES Users(UserID),
                        FOREIGN KEY (MenuID) REFERENCES Menus(MenuID)
                    );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Admin (
                        AdminID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Email TEXT,
                        Password TEXT,
                        Name TEXT
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
                        Rating INTEGER DEFAULT 0,
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
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS CART (
                        menuid INTEGER,
                        customerid INTEGER,
                        Instructions TEXT,
                        FOREIGN KEY (menuid) REFERENCES Menus (MenuID),
                        FOREIGN KEY (customerid) REFERENCES Customers (CustomerID)
                    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (
                        orderid INTEGER PRIMARY KEY AUTOINCREMENT,
                        menuid INTEGER,
                        customerid INTEGER,
                        status TEXT,
                        quantity INTEGER,
                        instructions TEXT,
                        Date TEXT,
                        FOREIGN KEY (menuid) REFERENCES Menus (MenuID),
                        FOREIGN KEY (customerid) REFERENCES Customers (CustomerID)
                    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Ratings (
                        RatingID INTEGER PRIMARY KEY AUTOINCREMENT,
                        OrderID INTEGER,
                        CustomerID INTEGER,
                        MenuID INTEGER,
                        Rating INTEGER,
                        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
                        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
                        FOREIGN KEY (MenuID) REFERENCES Menus(MenuID)
                    );''')

def insert_user(email, password, name=None, address=None, phone=None, registration_date=None):
    try:
        cursor.execute('''INSERT INTO Customers (Email, Password, Name, Address, Phone, RegistrationDate)
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

def insert_default_admin():
    try:
        cursor.execute('''SELECT * FROM Admin;''')
        admin_data = cursor.fetchone()
        
        if not admin_data:
            cursor.execute('''INSERT INTO Admin (Email, Password, Name) VALUES (?, ?, ?);''',
                           ['bilalahmad@gmail.com', '1234567', 'Bilal Ahmad'])
            connection.commit()
    except Exception as e:
        print(f"Error inserting default admin: {str(e)}")

def get_admin_name(email):
    try:
        cursor.execute('''SELECT name FROM Admin where email=?;''',[email])
        return cursor.fetchall()
    except Exception as e:
        print(str(e))
        return []

def get_all_Customers():
    try:
        cursor.execute('''SELECT * FROM Customers;''')
        return cursor.fetchall()
    except Exception as e:
        print(str(e))
        return []

def get_all_restaurants():
    try:
        cursor.execute('''SELECT * FROM Restaurants;''' )
        return cursor.fetchall()
    except Exception as e:
        print(str(e))
        return []


def get_all_cart(Customermail):
    try:
        cursor.execute('''SELECT CustomerID from Customers where Email = ?;''', [Customermail])
        id = cursor.fetchone()[0]
        cursor.execute('''SELECT m.ItemName, m.Price, p.Discount, m.ImagePNG, c.Instructions 
                          FROM CART c 
                          JOIN Menus m ON c.menuid = m.MenuID 
                          LEFT JOIN Promotions p ON c.menuid = p.MenuID 
                          WHERE c.customerid = ?;''', [id])
        cart_items = cursor.fetchall()
        print(cart_items)
        items_with_discounts = []
        for item in cart_items:
            item_name, price, discount, image, instructions = item
            if discount is not None:  # Check if the item has an active promotion
                discounted_price = price * (1 - discount / 100)  # Calculate discounted price
            else:
                discounted_price = 0  # If no discount, set discounted price to 0
            items_with_discounts.append({
                'ItemName': item_name,
                'OriginalPrice': price,
                'DiscountedPrice': discounted_price,
                'ImagePNG': image,
                'Instructions': instructions
            })
        return items_with_discounts
    except Exception as e:
        print(str(e))
        return []

def Add_new_admin(email,password,name):
    try:
        cursor.execute('''INSERT INTO Admin (Email, Password, Name)
                          VALUES (?, ?, ?);''',
                       [email, password, name])
        connection.commit()
        return ''
    except Exception as e:
        return f'Error: {str(e)}'


def blockResturant(resturantID,adminMail):
    try:
        cursor.execute("SELECT AdminID FROM Admin WHERE Email = ?", (adminMail))
        admin_row = cursor.fetchone()
        if admin_row:
            adminID = admin_row[0]

            cursor.execute("UPDATE Restaurants SET Blocked = 1, BlockedByAdmin = ? WHERE RestaurantID = ?", [adminID, resturantID])
            connection.commit()
            return True  
        else:
            return False 
    except Exception as e:
        print(e)
        return False

def blockUser(CustomerID,adminMail):
    try:
        cursor.execute("SELECT AdminID FROM Admin WHERE Email = ?", (adminMail))
        admin_row = cursor.fetchone()
        if admin_row:
            adminID = admin_row[0]

            cursor.execute("UPDATE Customers SET Blocked = 1, BlockedByAdmin = ? WHERE CustomerID = ?", [adminID, CustomerID])
            connection.commit()
            return True  
        else:
            return False 
    except Exception as e:
        print(e)
        return False
    
def unblockUser(CustomerID):
    try:
        cursor.execute("UPDATE Customers SET Blocked = 0, BlockedByAdmin = NULL WHERE CustomerID = ?", [CustomerID])
        connection.commit()
        return True  
    except Exception as e:
        print( e)
        return False

    
def unblockResturant(CustomerID):
    try:
        cursor.execute("UPDATE Restaurants SET Blocked = 0, BlockedByAdmin = NULL WHERE CustomerID = ?", [CustomerID])
        connection.commit()
        return True  
    except Exception as e:
        print( e)
        return False

def get_All_admins():
    try: 
        cursor.execute('''SELECT NAME , EMAIL FROM ADMIN;''')   
        return cursor.fetchall()
    except Exception as e:
        return str(e) 

def removeAdmin(name,email):
    try:
        cursor.execute('''DELETE FROM Admin where name=? and email=?;''',[email, name])
        connection.commit()
        return ''
    except Exception as e:
        return f'Error: {str(e)}'


def email_exists(email):
    try:
        cursor.execute("SELECT * FROM Customers WHERE Email=?;", [email])
        user_data = cursor.fetchone()


        if user_data:
            return True

        cursor.execute("SELECT * FROM Restaurants WHERE Email=?;", [email])
        restaurant_data = cursor.fetchone()
        if restaurant_data:
            return True

        return False
    except Exception as e:
        print(str(e))
        return None
    

def login_check(email,password):
    if email == None or password == None:
        return 'Enter Values'
    try:
        cursor.execute('''SELECT * FROM Customers Where email=? AND password =?;''',[email,password])
        user_data = cursor.fetchone()
        if user_data:
                #check for blocked or not
            return 'Customer'

        cursor.execute('''SELECT * FROM Restaurants Where email=? AND password =?;''',[email,password])
        user_data = cursor.fetchone()
        if user_data:
            return 'Restaurant'

        cursor.execute('''SELECT * FROM Admin Where email=? AND password =?;''',[email,password])
        user_data = cursor.fetchone()
        if user_data:
            return 'admin'
        return 'No data found with this email and password'
    except Exception as e:
        return f'Error: {str(e)}'

def login_check_Admin(email,password):
    if email == None or password == None:
        return 'Enter Values'
    try:
        cursor.execute('''SELECT * FROM Admin Where email=? AND password =?;''',[email,password])
        user_data = cursor.fetchone()
        if user_data:
            return 'admin'
        else:
            return 'Not an Admin'
        
    except Exception as e:
        return f'Error: {str(e)}'


def EmailCheck(email):
    try:
        cursor.execute('''SELECT * FROM Customers Where email=?;''',[email])
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


def addToCart(menu_title,Description,Price,CustomerEmail,instructions=''):
    try:
        cursor.execute('''SELECT MenuID FROM Menus where ItemName=? and Description=? and Price=?;''',[menu_title,Description,Price])
        id = cursor.fetchone()[0]
        cursor.execute('''SELECT CustomerID FROM Customers where Email=?;''',[CustomerEmail])
        Cid = cursor.fetchone()[0]
        cursor.execute('''SELECT * FROM Cart where Menuid=? and CustomerId =?;''',[id,Cid])
        if cursor.fetchall():
            return 'Item already added'
        cursor.execute('''INSERT INTO Cart (Menuid, CustomerId, Instructions)VALUES (?, ?, ?);''',[id,Cid,instructions])
        connection.commit()
        return 'Item added to cart successfully!'
    except Exception as e:
        print(str(e))
        return 'Database error'       


def addToCartPromotion(PromotionTitle,discounts,CustomerEmail,instructions=''):
    try:
        cursor.execute('''SELECT MenuID FROM Promotions where PromotionName=? and Discount=?;''',[PromotionTitle,discounts])
        id = cursor.fetchone()[0]
        cursor.execute('''SELECT CustomerID FROM Customers where Email=?;''',[CustomerEmail])
        Cid = cursor.fetchone()[0]
        cursor.execute('''SELECT * FROM Cart where Menuid=? and CustomerId =?;''',[id,Cid])
        if cursor.fetchall():
            return 'Item already added'
        cursor.execute('''INSERT INTO Cart (Menuid, CustomerId, Instructions)VALUES (?, ?, ?);''',[id,Cid,instructions])
        connection.commit()
        return 'Item added to cart successfully!'
    except Exception as e:
        print(str(e))
        return 'Database error' 


def get_menu_data(limit=100,all=False):
    try:
        if all:
            cursor.execute('''SELECT ItemName, Description, Price, ImagePNG ,Category  FROM Menus;''')
        else:    
            cursor.execute('''SELECT ItemName, Description, Price, ImagePNG ,Category  FROM Menus LIMIT ?''',[limit])
        return cursor.fetchall()
    except sqlite3.Error as e:
        print("Error fetching data from database:", e)
        return []


def get_favourite_data(customerEmail):
    try:
        cursor.execute("SELECT CustomerID FROM Customers WHERE Email = ?", [customerEmail])
        CustomerID = cursor.fetchone()
        if CustomerID is None:
            return []  

        cursor.execute('''SELECT m.ItemName, m.Price, m.Description, m.ImagePNG 
                          FROM Favourites f
                          JOIN Menus m ON f.MenuID = m.MenuID
                          WHERE f.CustomerID = ?''', [CustomerID[0]])
        favorite_items = cursor.fetchall()

        filtered_favorite_items = []
        for item in favorite_items:
            cursor.execute('''SELECT r.Blocked 
                              FROM Menus m
                              JOIN Restaurants r ON m.RestaurantID = r.RestaurantID
                              WHERE m.ItemName = ?''', [item[0]])
            restaurant_blocked = cursor.fetchone()
            if restaurant_blocked is None or restaurant_blocked[0] == 0:
                filtered_favorite_items.append(item)

        return filtered_favorite_items
    except Exception as e:
        print(str(e))
        return []


def getItemSearch(name):
    try:
        cursor.execute('''SELECT ItemName, Description, Price, ImagePNG, Category FROM Menus WHERE ItemName LIKE ? OR Category LIKE ?;''', ['%' + name + '%','%' + name + '%'])
        return cursor.fetchall()
    except sqlite3.Error as e:
        print("Error fetching data from database:", e)
        return []


def get_active_promotions(current_date,limit=100,all=False):
    try:
        if all:
            cursor.execute("""SELECT p.PromotionName, m.Price, p.Discount, m.ImageJPG FROM Promotions p JOIN Menus m ON p.MenuID = m.MenuID
                        WHERE p.StartDate <= ? AND p.EndDate >= ?""", [current_date, current_date])
        else:
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
        
        return []


    

def close_connection():
    connection.close()
