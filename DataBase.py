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
                        Image TEXT,
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
                        CustomerID INTEGER,
                        MenuID INTEGER,
                        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE,
                        FOREIGN KEY (MenuID) REFERENCES Menus(MenuID) ON DELETE CASCADE
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
                        FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID) ON DELETE CASCADE
                    );''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Promotions (
                        PromotionID INTEGER PRIMARY KEY AUTOINCREMENT,
                        PromotionName TEXT,
                        MenuID INTEGER,
                        Description TEXT,
                        Discount REAL,
                        StartDate TEXT,
                        EndDate TEXT,
                        FOREIGN KEY (MenuID) REFERENCES Menus (MenuID) ON DELETE CASCADE
                    );''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS CART (
                        menuid INTEGER,
                        customerid INTEGER,
                        Instructions TEXT,
                        quantity INTEGER DEFAULT 1,
                        FOREIGN KEY (menuid) REFERENCES Menus (MenuID) ON DELETE CASCADE,
                        FOREIGN KEY (customerid) REFERENCES Customers (CustomerID) ON DELETE CASCADE
                    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (
                        orderid INTEGER PRIMARY KEY AUTOINCREMENT,
                        menuid INTEGER,
                        customerid INTEGER,
                        status TEXT,
                        quantity INTEGER,
                        instructions TEXT,
                        Type TEXT,
                        Date TEXT,
                        FOREIGN KEY (menuid) REFERENCES Menus (MenuID) ON DELETE CASCADE,
                        FOREIGN KEY (customerid) REFERENCES Customers (CustomerID) ON DELETE SET NULL
                    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Ratings (
                        RatingID INTEGER PRIMARY KEY AUTOINCREMENT,
                        OrderID INTEGER,
                        CustomerID INTEGER,
                        MenuID INTEGER,
                        Rating INTEGER,
                        Comment TEXT,
                        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
                        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE SET NULL,
                        FOREIGN KEY (MenuID) REFERENCES Menus(MenuID) ON DELETE CASCADE
                    );''')


#user display 
def get_menu_data(limit=100,all=False):
    try:
        if all:
            cursor.execute('''SELECT ItemName, M.Description, Price, ImagePNG ,Category ,Rating FROM Menus M
                              INNER JOIN Restaurants R ON M.RestaurantID = R.RestaurantID
                              WHERE R.Blocked = 0;''')
        else:    
            cursor.execute('''SELECT ItemName, M.Description, Price, ImagePNG ,Category ,Rating  FROM Menus M INNER JOIN Restaurants R 
                              ON M.RestaurantID = R.RestaurantID
                              WHERE R.Blocked = 0 LIMIT ?;''',[limit])
        return cursor.fetchall()
    except sqlite3.Error as e:
        print("Error fetching data from database:", e)
        return []

# User display
def get_active_promotions(current_date,limit=100,all=False,png=False):
    try:
        if all and png:
            cursor.execute("""SELECT p.PromotionName, m.Price, p.Discount, m.ImagePNG, m.ItemName 
                                FROM Promotions p 
                                JOIN Menus m ON p.MenuID = m.MenuID
                                JOIN Restaurants r ON m.RestaurantID = r.RestaurantID
                                WHERE r.Blocked = 0 AND p.StartDate <= ? 
                                AND p.EndDate >= ?;""", [current_date, current_date])
        else:
            cursor.execute("""SELECT p.PromotionName, m.Price, p.Discount, m.ImageJPG, m.ItemName 
                                FROM Promotions p 
                                JOIN Menus m ON p.MenuID = m.MenuID
                                JOIN Restaurants r ON m.RestaurantID = r.RestaurantID
                                WHERE r.Blocked = 0 AND p.StartDate <= ? 
                                AND p.EndDate >= ? Limit ?;""", [current_date, current_date,limit])
        rows = cursor.fetchall()
        promotions_data = []
        for row in rows:
            promotion_name, price, discount, image ,itemName= row
            discounted_price = price * (1 - discount / 100)
            promotions_data.append({'PromotionName': promotion_name,'Price': price,'Discount': discount,'Image': image,'DiscountedPrice': discounted_price,'itemName':itemName})
        return promotions_data
    except sqlite3.Error as e:
        print("Error fetching data from database:", e)
        
        return []




# order status = pending , complete , in progress

def Update_status(orderID,status):
    try:
        cursor.execute('''UPDATE Orders SET status=? where orderID=?''',
                                [status,orderID])
        
        connection.commit()
        return 'Status updated successfully!'
    except sqlite3.Error as e:
        print("Database error:", e)
        return 'Database error'

def get_pending_orders(RestaurantID):
    try:
        cursor.execute('''SELECT M.ItemName, O.orderid, O.menuid, O.customerid, O.status, O.quantity, O.instructions, O.Type, O.Date, R.Rating,C.address
                          FROM Orders O
                          INNER JOIN Menus M ON O.menuid = M.MenuID
                          LEFT JOIN Ratings R ON O.orderid = R.OrderID
                          join Customers C on O.customerid = C.customerid 
                          WHERE o.status <> 'complete' AND M.RestaurantID = ?; ''',[RestaurantID])

        order_details = cursor.fetchall()

        order_details_list = []
        for item in order_details:
            item_dict = {
                'ItemName': item[0],
                'orderid': item[1],
                'menuid': item[2],
                'customerid': item[3],
                'status': item[4],
                'quantity': item[5],
                'instructions': item[6],
                'Type': item[7],
                'Date': item[8],
                'rating': item[9],
                'address': item[9]
            }
            order_details_list.append(item_dict)
        return order_details_list
    except sqlite3.Error as e:
        print("Database error:", e)
        return []


def get_Completed_orders(RestaurantID):
    try:
        cursor.execute('''SELECT M.ItemName, O.orderid, O.menuid, C.Name, O.status, O.quantity, O.instructions, O.Type, O.Date, R.Rating, C.address
                            FROM Orders O
                            INNER JOIN Menus M ON O.menuid = M.MenuID
                            LEFT JOIN Ratings R ON O.orderid = R.OrderID
                            JOIN Customers C ON C.Customerid = O.customerid
                            WHERE O.status = 'complete' AND M.RestaurantID = ?; ''',[RestaurantID])

        order_details = cursor.fetchall()

        order_details_list = []
        for item in order_details:
            item_dict = {
                'ItemName': item[0],
                'orderid': item[1],
                'menuid': item[2],
                'customerName': item[3],
                'status': item[4],
                'quantity': item[5],
                'instructions': item[6],
                'Type': item[7],
                'Date': item[8],
                'rating': item[9],
                'address': item[10]
            }
            order_details_list.append(item_dict)
        return order_details_list
    except sqlite3.Error as e:
        print("Database error:", e)
        return []

def updatePromotion(promoName,menuId,description,Discount,StartDate,endDate,promotionid,RestaurantID):
    try:
        cursor.execute('''SELECT menuid FROM Promotions where promotionid=?''',
                                [promotionid])
        result = cursor.fetchone()
        cursor.execute('''SELECT * FROM menus where menuid=? and restaurantid=?''',
                                [menuId,RestaurantID])
        result = cursor.fetchone()
        if result:
            
            cursor.execute('''UPDATE Promotions SET PromotionName=?, MenuID=?, Description=?, Discount=?, StartDate=?, EndDate=? where promotionid=?''',
                                [promoName,menuId,description,Discount,StartDate,endDate,promotionid])
            connection.commit()
            return 'Promotion updated successfully!'
        else:
            return 'Cannot access that Promotion'
    except sqlite3.Error as e:
        print("Database error:", e)
        return 'Database error'

def get_all_Promotions(RestaurantID):
    try:
        cursor.execute('''SELECT p.PromotionID, p.PromotionName, p.MenuID, p.Description, p.Discount, p.StartDate, p.EndDate
                          FROM Promotions p
                          INNER JOIN Menus m ON p.MenuID = m.MenuID
                          WHERE m.RestaurantID = ?''', [RestaurantID])
        promotions = cursor.fetchall()
        return promotions
    except Exception as e:
        print(str(e))
        return []

def addpromotion(MenuID,restaurantid,PromotionName,Description,Discount,StartDate,EndDate):
    try:
        cursor.execute('''SELECT RestaurantID FROM Menus WHERE Menuid=?''', [MenuID])
        ans = cursor.fetchone()[0]
        
        if ans!=restaurantid:
            return 'Cannot add promotion'
        else:
            cursor.execute('''INSERT INTO Promotions (PromotionName, MenuID, Description, Discount, StartDate, EndDate) VALUES (?, ?, ?, ?, ?, ?)''',
                                [PromotionName,MenuID,Description,Discount,StartDate,EndDate])
        
        connection.commit()
        return 'Promotion added successfully!'
    except sqlite3.Error as e:
        print("Database error:", e)
        return 'Database error'


def is_customer(id,email,password):
    try:
        cursor.execute('''SELECT * FROM Customers where CustomerID=? AND email = ? AND password=?;''',[id,email,password])
        ans = cursor.fetchone()
        if ans:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def is_Restaurant(id,email,password):
    try:
        cursor.execute('''SELECT * FROM Restaurants where RestaurantID=? AND email = ? AND password=?;''',[id,email,password])
        ans = cursor.fetchone()
        if ans:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def is_Admin(id):
    try:
        cursor.execute('''SELECT * FROM Admin where AdminID=?;''',[id])
        ans = cursor.fetchone()
        if ans:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def addItem(ItemName,Description,RestaurantID,Price,Category,ImageJPG,ImagePNG):
    try:
        cursor.execute('''SELECT * FROM Menus WHERE ItemName = ? AND Description=? AND Price=? AND Category=? AND RestaurantID=?''', [ItemName,Description,Price,Category,RestaurantID])
        existing_item = cursor.fetchone()
        
        if existing_item:
            return 'Already exists'
        else:
            cursor.execute('''INSERT INTO Menus (ItemName, Description, Price, Category, ImagePNG, ImageJPG, RestaurantID) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                                [ItemName,Description,Price,Category,ImagePNG,ImageJPG,RestaurantID])
        
        connection.commit()
        return 'Item added successfully!'
    except sqlite3.Error as e:
        print("Database error:", e)
        return 'Database error'

def updateItem(ItemName,Description,RestaurantID,menuid,Price,Category,ImageJPG,ImagePNG):
    try:
        cursor.execute('''UPDATE Menus SET ItemName=?, Description=?, Price=?, Category=?, ImagePNG=?, ImageJPG=? where menuid=? and restaurantid=?''',
                                [ItemName,Description,Price,Category,ImagePNG,ImageJPG,menuid,RestaurantID])
        
        connection.commit()
        return 'Item updated successfully!'
    except sqlite3.Error as e:
        print("Database error:", e)
        return 'Database error'




def removeItem(itemid,Restaurantid):
    try:
        cursor.execute('''SELECT Restaurantid FROM Menus where menuid=?;''',[itemid])
        result = cursor.fetchone()
        if result:
            if result[0] == Restaurantid:
                cursor.execute('''DELETE FROM Menus where menuid=? AND Restaurantid=?;''',[itemid,Restaurantid])
                connection.commit()
                return 'Deleted!'
        else:
                return 'Cannot delete this item'
    except Exception as e:
        print(str(e))
        return 'Database error' 

def removePromotion(promotionid,Restaurantid):
    try:
        cursor.execute('''SELECT menuid FROM Promotions where promotionid=?;''',[promotionid])
        result = cursor.fetchone()
        if result:
            cursor.execute('''SELECT RestaurantID FROM Menus where menuid=?;''',[result[0]])
            result = cursor.fetchone()
            if result[0] == Restaurantid:
                cursor.execute('''DELETE FROM Promotions where promotionid=?;''',[promotionid])
                connection.commit()
                return 'Deleted!'
        else:
                return 'Cannot delete this Promotion'
    except Exception as e:
        print(str(e))
        return 'Database error' 


def get_Item(id,RestaurantID):
    try:
        cursor.execute('''SELECT * FROM Menus where Menuid = ? AND RestaurantID=?;''',[id,RestaurantID])
        return cursor.fetchone()
    except Exception as e:
        print(str(e))
        return []

def get_Promotion(id,RestaurantID):
    try:
        cursor.execute('''SELECT * FROM Promotions where Promotionid = ?;''',[id])
        ans = cursor.fetchone()
        cursor.execute('''SELECT * FROM Menus where Menuid = ? AND RestaurantID=?;''',[ans[2],RestaurantID])
        check = cursor.fetchone()
        if check:
            return ans
        else:
            return []
    except Exception as e:
        print(str(e))
        return []

def get_Items_ofRestaurant(RestaurantID):
    try:
        cursor.execute('''SELECT * FROM Menus where RestaurantID=?;''',[RestaurantID])
        return cursor.fetchall()
    except Exception as e:
        print(str(e))
        return []


def get_customer_info(id):
    try:
        cursor.execute('''SELECT Email,Password,Name,Address,Phone,Image FROM Customers where Customerid = ?;''',[id])
        return cursor.fetchone()
    except Exception as e:
        print(str(e))
        return []
    
def get_resturant_info(id):
    try:
        cursor.execute('''SELECT Email,Password,Name,Description,Address,Phone,Website,OpeningHours FROM Restaurants where RestaurantID = ?;''',[id])
        return cursor.fetchone()
    except Exception as e:
        print(str(e))
        return []


def UpdateCustomer(name,email,password,phone,imageName,address,id):
    try:
        cursor.execute('''UPDATE Customers SET Email = ?, Password = ?, Name = ?, Address = ?, Phone = ?, Image = ? WHERE Customerid = ?;''',
                       [email, password, name, address, phone, imageName, id])
        connection.commit()
        return 'success'
    except Exception as e:
        return f'Error: {str(e)}'



def UpdateResturant(name,email,website,description,password,phone,hours,address,id):
    try:
        cursor.execute('''UPDATE Restaurants SET Email = ?,description=?, Password = ?, Name = ?, Address = ?, Phone = ?, website = ?, OpeningHours = ? WHERE Restaurantid = ?;''',
                       [email,description, password, name, address, phone, website,hours, id])
        connection.commit()
        return 'success'
    except Exception as e:
        return f'Error: {str(e)}'


def insert_user(email, password, name=None, address=None, phone=None, registration_date=None,image='default.jpg'):
    try:
        cursor.execute('''INSERT INTO Customers (Email, Password, Name, Address, Phone, RegistrationDate,Image)
                          VALUES (?, ?, ?, ?, ?, ?);''',
                       [email, password, name, address, phone, registration_date,image])
        connection.commit()
        cursor.execute('''Select CustomerID From Customers where email=? AND password=?;''',[email, password])
        
        return cursor.fetchone()[0]
    except Exception as e:
        return f'Error: {str(e)}'

def insert_restaurants(email, password, name=None, address=None, phone=None, registration_date=None):
    try:
        cursor.execute('''INSERT INTO Restaurants (Email, Password, Name, Address, Phone, RegistrationDate)
                      VALUES (?, ?, ?, ?, ?, ?);''',
                   [email, password, name, address, phone, registration_date])
        connection.commit()
        cursor.execute('''Select RestaurantID From Restaurants where email=? AND password=?;''',[email, password])
        
        return cursor.fetchone()[0]
    except Exception as e:
        return f'Error: {str(e)}'

def get_customer_id(email,password):
    try:
        cursor.execute('''Select CustomerID From Customers where email=? AND password=?;''',[email, password])
        return cursor.fetchone()[0]
    except Exception as e:
        return f'Error: {str(e)}'

def get_restaurants_id(email,password):
    try:
        cursor.execute('''Select RestaurantId From Restaurants where email=? AND password=?;''',[email, password])
        return cursor.fetchone()[0]
    except Exception as e:
        return f'Error: {str(e)}'

def getResturantName(resturantid):
    try:
        cursor.execute('''Select Name From Restaurants where RestaurantId=?;''',[resturantid])
        return cursor.fetchone()[0]
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

def get_a_restaurant(id):
    try:
        cursor.execute('''SELECT * FROM Restaurants where RestaurantID=?;''',[id])
        return cursor.fetchone()
    except Exception as e:
        print(str(e))
        return []

def get_active_restaurants():
    try:
        cursor.execute('''SELECT * FROM Restaurants where Blocked = 0;''' )
        return cursor.fetchall()
    except Exception as e:
        print(str(e))
        return []

def get_all_cart(Customerid):
    try:
        cursor.execute('''SELECT m.ItemName, m.Price, p.Discount, m.ImagePNG, c.Instructions ,m.Menuid , c.quantity
                          FROM CART c 
                          JOIN Menus m ON c.menuid = m.MenuID 
                          LEFT JOIN Promotions p ON c.menuid = p.MenuID 
                          WHERE c.customerid = ?;''', [Customerid])
        cart_items = cursor.fetchall()
        items_with_discounts = []
        for item in cart_items:
            item_name, price, discount, image, instructions ,menuid,quantity= item
            if discount is not None:  
                discounted_price = price * (1 - discount / 100)
            else:
                discounted_price = price  
            items_with_discounts.append({
                'ItemName': item_name,
                'OriginalPrice': price,
                'DiscountedPrice': discounted_price,
                'ImagePNG': image,
                'Instructions': instructions,
                'menuid':menuid,
                'quantity':quantity
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

def placeOrder(customerid,date,Type):
    try:
        cursor.execute('''INSERT INTO Orders (menuid, customerid, status, quantity, instructions, Date,Type)
                          SELECT menuid, customerid, 'pending', quantity, Instructions, ? ,?
                          FROM CART WHERE customerid = ?''', [date,Type,customerid])
        
        cursor.execute('''DELETE FROM CART WHERE customerid = ?''', [customerid])
        
        connection.commit()
        
        return 'Order placed successfully!'
    except Exception as e:
        print(str(e))
        return 'Database error'



def get_order_details(customer_id):
    try:
        cursor.execute('''SELECT O.orderid, M.ItemName, M.ImageJPG, O.quantity, O.Date, O.status, R.Rating, R.Comment, O.instructions, M.price,M.Menuid
                          FROM Orders O
                          INNER JOIN Menus M ON O.menuid = M.MenuID
                          LEFT JOIN Ratings R ON O.orderid = R.OrderID
                          WHERE O.customerid = ?''', (customer_id,))
        
        
        order_details = cursor.fetchall()

        order_details_list = []
        for item in order_details:
            
            order_id, item_name, image_jpg, quantity, order_date, status, rating, comment, instructions, price,menuid = item

            discount = get_discount_for_item_on_date(menuid, order_date)
            if discount is not None:
                discounted_price = price * (1 - discount / 100)
                price = discounted_price
            item_dict = {
                'OrderID': order_id,
                'ItemName': item_name,
                'ImageJPG': image_jpg,
                'Quantity': quantity,
                'Date': order_date,
                'Status': status,
                'Rating': rating,
                'Comment': comment,
                'Instructions': instructions,
                'Price': price
            }
            order_details_list.append(item_dict)
        
        return order_details_list
    except sqlite3.Error as e:
        print("Database error:", e)
        return None

def get_discount_for_item_on_date(menuid, order_date):
    try:
        cursor.execute('''SELECT p.Discount
                          FROM Promotions p
                          WHERE menuid = ? AND ? BETWEEN p.StartDate AND p.EndDate''', (menuid, order_date))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except sqlite3.Error as e:
        print("Database error:", e)
        return None
    



def blockResturant(resturantID,adminMail):
    try:
        print(resturantID,adminMail)
        cursor.execute("SELECT AdminID FROM Admin WHERE Email = ?", [adminMail])
        admin_row = cursor.fetchone()
        if admin_row:
            adminID = admin_row[0]
            print(adminID)
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
        print(adminMail,CustomerID)
        cursor.execute("SELECT AdminID FROM Admin WHERE Email = ?", [adminMail])
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



def unblockResturant(resturantID):
    try:
        cursor.execute("UPDATE Restaurants SET Blocked = 0, BlockedByAdmin = NULL WHERE RestaurantID = ?", [resturantID])
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
        cursor.execute('''SELECT * FROM Customers Where email=? AND password =? AND blocked=0;''',[email,password])
        user_data = cursor.fetchone()
        if user_data:
                #check for blocked or not
            return 'Customer'

        cursor.execute('''SELECT * FROM Restaurants Where email=? AND password =? AND blocked =0;''',[email,password])
        user_data = cursor.fetchone()
        if user_data:
            return 'Restaurant'
        
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


def EmailCheck(id):
    try:
        cursor.execute('''SELECT * FROM Customers Where email=?;''',[id])
        user_data = cursor.fetchone()
        if user_data:
            return 'User'

        cursor.execute('''SELECT * FROM Restaurants Where email=?;;''',[id])
        user_data = cursor.fetchone()
        if user_data:
            return 'Restaurant'

        return 'No data found with this email and password'
    except Exception as e:
        return f'Error: {str(e)}'


def addToCart(menu_title,Description,Price,Customerid,instructions=' '):
    try:
        print('in cart')
        print(menu_title,Description,Price)
        
        cursor.execute('''SELECT MenuID FROM Menus where ItemName=? and Description=? and Price=?;''',[menu_title,Description,Price])
        id = cursor.fetchone()[0]
        print(id)
        cursor.execute('''SELECT * FROM Cart where Menuid=? and CustomerId =?;''',[id,Customerid])
        if cursor.fetchall():
            return 'Item already added'
        print('i am here')
        cursor.execute('''INSERT INTO Cart (Menuid, CustomerId, Instructions)VALUES (?, ?, ?);''',[id,Customerid,instructions])
        connection.commit()
        return 'Item added to cart successfully!'
    except Exception as e:
        print(str(e))
        return 'Database error'       


def addToCartPromotion(PromotionTitle,discounts,Customerid,instructions=''):
    try:
        print('in function add to cart promotion')
        if discounts != 0:
            cursor.execute('''SELECT MenuID FROM Promotions where PromotionName=? and Discount=?;''',[PromotionTitle,discounts])
        else:
            cursor.execute('''SELECT MenuID FROM Promotions where PromotionName=?;''',[PromotionTitle])
        id = cursor.fetchone()[0]
        cursor.execute('''SELECT * FROM Cart where Menuid=? and CustomerId =?;''',[id,Customerid])
        if cursor.fetchall():
            return 'Item already added'
        cursor.execute('''INSERT INTO Cart (Menuid, CustomerId, Instructions)VALUES (?, ?, ?);''',[id,Customerid,instructions])
        connection.commit()
        return 'Item added to cart successfully!'
    except Exception as e:
        print(str(e))
        return 'Database error' 


def removeFromcart(menuid,Customerid):
    try:
        cursor.execute('''DELETE FROM CART where menuid=? AND customerid=?;''',[menuid,Customerid])
        connection.commit()
        return 'Deleted!'
    except Exception as e:
        print(str(e))
        return 'Database error' 
    
def UpdateFromcart(menuid, Customerid, instruction,quantity):
    try:
        cursor.execute('''UPDATE CART SET instructions=? , quantity=? WHERE menuid=? AND customerid=?;''', [instruction,quantity, menuid, Customerid])
        connection.commit()
        return 'item updated!'
    except Exception as e:
        print(str(e))
        return 'Database error'

def UpdateRating(Customerid,orderid, rating,comment):
    try:
        cursor.execute('''SELECT RatingID FROM Ratings WHERE OrderID = ? AND CustomerID = ?''', (orderid, Customerid))
        existing_rating = cursor.fetchone()
        if existing_rating:
            rating_id = existing_rating[0]
            cursor.execute('''UPDATE Ratings SET Rating = ?, Comment = ? WHERE RatingID = ?''', (rating, comment, rating_id))
        else:
            cursor.execute('''SELECT menuid FROM Orders WHERE orderid = ? AND customerid = ?''', (orderid, Customerid))
            menuid = cursor.fetchone()[0]
            cursor.execute('''INSERT INTO Ratings (OrderID, CustomerID, MenuID, Rating, Comment) VALUES (?, ?, ?, ?, ?)''',
                           (orderid, Customerid, menuid, rating, comment))

        connection.commit()
        return 'Rating updated successfully!'
    except sqlite3.Error as e:
        print("Database error:", e)
        return 'Database error'


def get_Menu_With_Id(ids):
    try:
        ans = []
        for id in ids:
            cursor.execute('''SELECT ItemName, m.Description, Price, ImagePNG, Category FROM Menus m Join 
                               Restaurants r on m.restaurantid = r.restaurantid WHERE r.blocked=0 AND Menuid = ?;''', [id])
            row = cursor.fetchone()  
            if row is not None:  
                ans.append(row)
        return ans
    except sqlite3.Error as e:
        print("Error fetching data from database:", e)
        return []




def get_favourite_data(CustomerID):
    try:
        cursor.execute('''SELECT m.ItemName, m.Price, m.Description, m.ImagePNG 
                          FROM Favourites f
                          JOIN Menus m ON f.MenuID = m.MenuID
                          join Restaurants r on r.restaurantid = m.restaurantid 
                          WHERE f.CustomerID = ?''', [CustomerID])
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
        cursor.execute('''SELECT M.ItemName, M.Description, M.Price, M.ImagePNG, M.Category FROM Menus M
                       join Restaurants R on M.restaurantID = R.restaurantID 
                       WHERE R.blocked = 0 AND (ItemName LIKE ? OR Category LIKE ?);''', ['%' + name + '%','%' + name + '%'])
        return cursor.fetchall()
    except sqlite3.Error as e:
        print("Error fetching data from database:", e)
        return []


def addToFavourites(Customerid,menu_title='',Description='',Price='',PromotionName=''):
    try:
        if PromotionName == '':
            cursor.execute('''SELECT MenuID FROM Menus where ItemName=? and Description=? and Price=?;''',[menu_title,Description,Price])
        else:
            cursor.execute('''SELECT MenuID FROM Promotions where PromotionName=?;''',[PromotionName])
            
        id = cursor.fetchone()[0]
       
        cursor.execute('''SELECT * FROM Favourites where Menuid=? and CustomerID =?;''',[id,Customerid])
        if cursor.fetchall():
            cursor.execute('''DELETE FROM Favourites where Menuid=? and CustomerId =?;''',[id,Customerid])
            return 'Item Removed from Favourites'
        
        cursor.execute('''INSERT INTO  Favourites (Menuid, CustomerId) VALUES (?, ?);''',[id,Customerid])
        connection.commit()
        return 'Item added to Favourites successfully!'
    except Exception as e:
        print(str(e))
        return 'Database error'  



def close_connection():
    connection.close()
