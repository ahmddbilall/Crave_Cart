from flask import Flask, render_template, redirect, request, session,flash,url_for
import secrets
import DataBase
import helpingFunctions
from datetime import date
import os
from werkzeug.utils import secure_filename

secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.secret_key = secret_key
app.config['UPLOAD_FOLDER'] = 'static/images'


  
  
        







# USER
      
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data = DataBase.get_menu_data(limit=6)
    Pro = DataBase.get_active_promotions(current_date=date.today().strftime("%Y-%m-%d"), limit=2)
    return render_template('user/home.html',menu_data=data,Promotions=Pro)



@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        input = request.form['search-input']
        data = DataBase.getItemSearch(name=input)
        if len(data) == 0:
            data = DataBase.get_menu_data(all=True)
            flash('Nothing found related to '+str(input),'error')
            dataView = 'all'
        else:
            dataView = input
    else:
        data = DataBase.get_menu_data(all=True)
        dataView = 'all'        
    return render_template('user/search.html', menu=data,dataView=dataView)


@app.route('/handle-Add-to-cart-from-search',methods=['GET','POST'])
def addToCartSearch():
    if 'username' not in session:
        return redirect('/login')
    menu_title = request.args.get('ItemName')
    Description = request.args.get('Description')
    Price = request.args.get('Price')
    Customerid = session['username'] 
    
    output = DataBase.addToCart(menu_title=menu_title,Description=Description,Price=Price,Customerid=Customerid)
    if output =='Item added to cart successfully!':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/search')


@app.route('/handle-Add-to-cart-from-recommend',methods=['GET','POST'])
def addToCartrecommend():
    if 'username' not in session:
        return redirect('/login')
    menu_title = request.args.get('ItemName')
    Description = request.args.get('Description')
    Price = request.args.get('Price')
    Customerid = session['username'] 
    
    output = DataBase.addToCart(menu_title=menu_title,Description=Description,Price=Price,Customerid=Customerid)
    if output =='Item added to cart successfully!':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/recommendation')

@app.route('/handle-Add-to-cart-from-favourite',methods=['GET','POST'])
def addToCartfavourite():
    if 'username' not in session:
        return redirect('/login')
    menu_titlee = request.args.get('ItemName')
    Descriptionn = request.args.get('Description')
    Pricee = request.args.get('Price')
    Customerid = session['username'] 
    print(menu_titlee,Descriptionn,Pricee)
    print(Descriptionn)
    output = DataBase.addToCart(menu_title=menu_titlee,Description=Descriptionn,Price=Pricee,Customerid=Customerid)
    if output =='Item added to cart successfully!':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/favourites')



@app.route('/handle-Add-to-cart-from-home',methods=['GET','POST'])
def addToCartHome():
    if 'username' not in session:
        return redirect('/login')
    
    menu_title = request.args.get('ItemName')
    Description = request.args.get('Description')
    Price = request.args.get('Price')
    Customerid = session['username'] 
    print(menu_title,Description,Price,Customerid)
    output = DataBase.addToCart(menu_title=menu_title,Description=Description,Price=Price,Customerid=Customerid)
    print(output)
    if output =='Item added to cart successfully!':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/home')


@app.route('/handle-Add-to-cart-Promotion-from-home',methods=['GET','POST'])
def addToCartPromotionHome():
    if 'username' not in session:
        return redirect('/login')
    
    PromotionTitle = request.args.get('PromotionName')
    discounts = request.args.get('discount')
    Customerid = session['username'] 
    
    output = DataBase.addToCartPromotion(PromotionTitle=PromotionTitle,discounts=discounts,Customerid=Customerid)
    if output =='Item added to cart successfully!':
        
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/home')



@app.route('/recommendation',methods=['GET','POST'])
def Recommendation():
    if 'username' not in session:
        return redirect('/login')
    query = False
    ans = False
    Data = []
    input=''
    if request.method == 'POST':
        input = request.form['item']
        query = True
        dataIds = helpingFunctions.recommend(input)
        if len(dataIds) == 0:
            flash('Nothing found related to '+str(input),'error')
            ans = False
        else:
            Data = DataBase.get_Menu_With_Id(dataIds)
            ans = True

    return render_template('user/recommendation.html',menu=Data,item_names=helpingFunctions.get_all_item_name(),query=query,ans=ans,name=input)


@app.route('/favourites')
def Favourites():
    if 'username' not in session:
        return redirect('/login')
    data =DataBase.get_favourite_data(session['username'])
    return render_template('user/favourites.html',menu=data,result=len(data))


@app.route('/handle-Add-to-favourite-from-home',methods=['GET','POST'])
def addToFavouriteHome():
    if 'username' not in session:
        return redirect('/login')
    
    menu_title = request.args.get('ItemName')
    Description = request.args.get('Description')
    Price = request.args.get('Price')
    Customerid = session['username'] 
    
    output = DataBase.addToFavourites(menu_title=menu_title,Description=Description,Price=Price,Customerid=Customerid)
    if output =='Item added to cart successfully!' or output == 'Item Removed from Favourites':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/home')



@app.route('/handle-remove-to-favourite-from-favourites',methods=['GET','POST'])
def removeFromFavourite():
    if 'username' not in session:
        return redirect('/login')
    
    menu_title = request.args.get('ItemName')
    Description = request.args.get('Description')
    Price = request.args.get('Price')
    Customerid = session['username'] 
    
    output = DataBase.addToFavourites(menu_title=menu_title,Description=Description,Price=Price,Customerid=Customerid)
    if output =='Item added to cart successfully!' or output == 'Item Removed from Favourites':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/favourites')

@app.route('/handle-Add-to-favourite-from-search',methods=['GET','POST'])
def addToFavouriteSearch():
    if 'username' not in session:
        return redirect('/login')
    
    menu_title = request.args.get('ItemName')
    Description = request.args.get('Description')
    Price = request.args.get('Price')
    Customerid = session['username'] 
    
    output = DataBase.addToFavourites(menu_title=menu_title,Description=Description,Price=Price,Customerid=Customerid)
    if output =='Item added to cart successfully!' or output == 'Item Removed from Favourites':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/search')

@app.route('/handle-Add-to-favourite-from-recommend',methods=['GET','POST'])
def addToFavouriterecommend():
    if 'username' not in session:
        return redirect('/login')
    
    menu_title = request.args.get('ItemName')
    Description = request.args.get('Description')
    Price = request.args.get('Price')
    Customerid = session['username'] 
    
    output = DataBase.addToFavourites(menu_title=menu_title,Description=Description,Price=Price,Customerid=Customerid)
    if output =='Item added to cart successfully!' or output == 'Item Removed from Favourites':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/recommendation')

@app.route('/handle-Add-to-fav-Promotion-from-discount',methods=['GET','POST'])
def addToFavouriteDiscount():
    if 'username' not in session:
        return redirect('/login')
    
    Promotion = request.args.get('PromotionName')
    Customerid = session['username'] 
    
    output = DataBase.addToFavourites(PromotionName=Promotion,Customerid=Customerid)
    if output =='Item added to cart successfully!' or output == 'Item Removed from Favourites':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/discounts')


@app.route('/handle-Add-to-cart-from-discount',methods=['GET','POST'])
def addToCartDiscount():
    if 'username' not in session:
        return redirect('/login')
    
    PromotionTitle = request.args.get('PromotionName')
    Customerid = session['username'] 
    print(PromotionTitle)
    output = DataBase.addToCartPromotion(PromotionTitle=PromotionTitle,discounts=0,Customerid=Customerid)
    if output =='Item added to cart successfully!':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/discounts')


@app.route('/discounts')
def discounts():
    if 'username' not in session:
        return redirect('/login')
    data= DataBase.get_active_promotions(current_date=date.today().strftime("%Y-%m-%d"),all=True,png=True)
    return render_template('user/discounts.html',data=data,result=len(data))

@app.route('/cart')
def cart():
    if 'username' not in session:
        return redirect('/login')
    
    dataa = DataBase.get_all_cart(session['username'])
    return render_template('user/cart.html',data=dataa)
  
  
@app.route('/handle-remove-from-cart',methods=['GET','POST'])
def removefromCart():
    if 'username' not in session:
        return redirect('/login')
    
    menuid = request.args.get('menuid')
    Customerid = session['username'] 
    output = DataBase.removeFromcart(menuid=menuid,Customerid=Customerid)
    if output =='Deleted!':
        flash('Item deleted from cart', 'success')
    else:
        flash(output, 'error')
    return redirect('/cart') 

@app.route('/handle-instruction-from-cart',methods=['GET','POST'])
def instructionfromCart():
    if 'username' not in session:
        return redirect('/login')
    
    menuid = request.args.get('menuid')
    instruction = request.args.get('instruction')
    quantity = request.args.get('quantity')
    Customerid = session['username'] 
    output = DataBase.UpdateFromcart(menuid=menuid,Customerid=Customerid,instruction=instruction,quantity=quantity)
    if output =='item updated!':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/cart') 

@app.route('/handle-order-from-cart',methods=['GET','POST'])
def orderfromCart():
    if 'username' not in session:
        return redirect('/login')
    
    Customerid = session['username'] 
    output = DataBase.placeOrder(customerid=Customerid,date=date.today().strftime("%Y-%m-%d"))
    if output =='Order placed successfully!':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/cart') 

 
  
@app.route('/')
def login_redirect():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect('/login')
    data = DataBase.get_customer_info(id = session['username'])
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password-input']
        phone = request.form['phone']
        address = request.form['address']
    
        file = request.files['image']
        if file:
            imageName = secure_filename(file.filename)
            if imageName:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], imageName))
        else:
            if data[5]!='default.jpg':
                imageName = data[5]
            else:
                imageName = 'default.jpg'
        DataBase.UpdateCustomer(name=name,email=email,password=password,phone=phone,imageName=imageName,address=address,id=session['username'])  
        data = DataBase.get_customer_info(id = session['username'])
    
    return render_template('user/profile.html',data=data)


@app.route('/trackorders')
def trackOrders():
    if 'username' not in session:
        return redirect('/login')

    data = DataBase.get_order_details(customer_id=session['username'])
    return render_template('user/trackorders.html',order_details=data,dataLength=len(data))

@app.route('/add-review',methods=['POST','GET'])
def addReview():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        rating = request.form['rating']
        comment = request.form['comment']
        order_id = request.form['order_id']
        DataBase.UpdateRating(Customerid=session['username'],orderid=order_id, rating=rating,comment=comment)
        
    
    return redirect('trackorders')


# resturant







@app.route('/restaurantHome')
def restaurantHome():
    if 'username' not in session:
        return redirect('/login')
    return render_template('restaurant/restaurantHome.html')







# Starts Admin functions 

@app.route('/admin')
def admin():
    if 'admin' in session:
        redirect(url_for('adminHome'))
    return redirect(url_for('adminlogin'))

@app.route('/adminHome')
def adminHome():
    if 'admin' not in session:
        return redirect('adminlogin')
    return render_template('admin/adminHome.html',name=DataBase.get_admin_name(session['admin']))

@app.route('/adminlogin',methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        status = DataBase.login_check_Admin(email=email,password=password)
        if status == 'admin':
            session['admin'] = email
            return redirect(url_for('adminHome'))  
        else:
            flash(status,'error')
    
    return render_template('admin/Adminlogin.html')

@app.route('/Add-new-admin',methods=['GET','POST'])
def AddNewadmin():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        status = DataBase.Add_new_admin(email=email,password=password,name=name)
    
        if status == '':
            flash(name + ' add as admin','success')
    return render_template('admin/AddnewAdmin.html')

@app.route('/remove-admin',methods=['GET','POST'])
def removeadmin():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    return render_template('admin/removeAdmin.html',admins = DataBase.get_All_admins())

@app.route('/handle-remove-admin',methods=['GET','POST'])
def handleremoveadmin():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    
    name = request.args.get('name')
    email = request.args.get('email')
     
    if (session['admin'] != 'bilalahmad@gmail.com') or (name == 'Bilal Ahmad' and email == 'bilalahmad@gmail.com'):
        flash('You are not allowed to remove admin','error') 
        return redirect('remove-admin')
    
    output = DataBase.removeAdmin(name=name,email=email)
    if output =='':
        flash(name + ' Removed successfully!', 'success')
    else:
        flash(output, 'error')
    
    return redirect('remove-admin')

@app.route('/All-Users')
def AllUsers():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    return render_template('admin/allusers.html',users=DataBase.get_all_Customers())

@app.route('/handle-block-user',methods=['GET','POST'])
def handleblockuser():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    
    id = request.args.get('id')
    
    output = DataBase.blockUser(CustomerID=id,adminMail=session['admin'])
    if output =='':
        flash('User blocked successfully!', 'success')
    else:
        flash(output, 'error')
    
    return redirect('All-Users')

@app.route('/handle-unblock-user',methods=['GET','POST'])
def handleunblockuser():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    
    id = request.args.get('id')
    
    output = DataBase.unblockUser(CustomerID=id)
    if output =='':
        flash('Resturant unblocked successfully!', 'success')
    else:
        flash(output, 'error')
    
    return redirect('All-Users')

@app.route('/All-Resturants')
def AllResturants():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    return render_template('admin/allresturants.html',resturants=DataBase.get_all_restaurants())

@app.route('/handle-block-resturant',methods=['GET','POST'])
def handleblockresturant():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    
    id = request.args.get('id')
    
    output = DataBase.blockResturant(resturantID=id,adminMail=session['admin'])
    if output =='':
        flash('Resturant blocked successfully!', 'success')
    else:
        flash(output, 'error')
    
    return redirect('All-Resturants')

@app.route('/handle-unblock-resturant',methods=['GET','POST'])
def handleunblockresturant():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    
    id = request.args.get('id')
    
    output = DataBase.unblockResturant(resturantID=id)
    if output =='':
        flash('Resturant unblocked successfully!', 'success')
    else:
        flash(output, 'error')
    
    return redirect('All-Resturants')

@app.route('/logoutAdmin')
def adminlogout():
    session.pop('admin',None)
    return redirect('/')

# End Admin



# Common for all users and resturants



@app.route('/Aboutus')
def aboutus():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('aboutus.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        account_type = request.form['account-type']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if not helpingFunctions.validate_email(email):
            flash('Invalid email format', 'error')
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash('Password and confirm password do not match', 'error')
            return redirect(url_for('signup'))
        

        if DataBase.email_exists(email):
            flash('Customer with this email already exists', 'error')
            return redirect(url_for('signup'))

        registration_date = date.today().strftime("%Y-%m-%d")
        if account_type == 'Customer':
            status =DataBase.insert_user(email=email,password=password,registration_date=registration_date)
            if isinstance(status, str):
                flash(status,'error')
            else:
                flash('Customer added successfully','success')
                session['username'] = status
                return redirect(url_for('home'))
        elif account_type == 'restaurant':
            status =DataBase.insert_restaurants(email=email,password=password,registration_date=registration_date)
            if isinstance(status, str):
                flash(status,'error')
            else:
                flash('Restaurant added successfully','success')
                session['username'] = status
                return redirect(url_for('home'))
    return render_template('signup.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        status = DataBase.login_check(email=email,password=password)
    
        if status == 'Customer' or status == 'Restaurant':
            currentUser = status
            if (currentUser == 'Customer'):
                session['username'] = DataBase.get_customer_id(email,password)
                return redirect(url_for('home'))
            else:
                session['username'] = DataBase.get_restaurants_id(email,password)
                return redirect(url_for('restaurantHome'))
        else:
            flash(status,'error')
    return render_template('login.html')




if __name__ == '__main__':
    DataBase.create_tables()
    DataBase.insert_default_admin()
    app.run(debug=True, port=5001)
    
