from flask import Flask, render_template, redirect, request, session,flash,url_for
import secrets
import DataBase
import helpingFunctions
from datetime import date


secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.secret_key = secret_key

        

# USER
      
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data = DataBase.get_menu_data(limit=10)
    Pro = DataBase.get_active_promotions(current_date=date.today().strftime("%Y-%m-%d"), limit=2)
    return render_template('home.html',menu_data=data,Promotions=Pro)



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
    return render_template('search.html', menu=data,dataView=dataView)


@app.route('/handle-Add-to-cart-from-search',methods=['GET','POST'])
def addToCartSearch():
    if 'username' not in session:
        return redirect('/login')
    menu_title = request.args.get('ItemName')
    Description = request.args.get('Description')
    Price = request.args.get('Price')
    CustomerEmail = session['username'] 
    
    output = DataBase.addToCart(menu_title=menu_title,Description=Description,Price=Price,CustomerEmail=CustomerEmail)
    if output =='Item added to cart successfully!':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/search')


@app.route('/handle-Add-to-cart-from-home',methods=['GET','POST'])
def addToCartHome():
    if 'username' not in session:
        return redirect('/login')
    
    menu_title = request.args.get('ItemName')
    Description = request.args.get('Description')
    Price = request.args.get('Price')
    CustomerEmail = session['username'] 
    
    output = DataBase.addToCart(menu_title=menu_title,Description=Description,Price=Price,CustomerEmail=CustomerEmail)
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
    CustomerEmail = session['username'] 
    
    output = DataBase.addToCartPromotion(PromotionTitle=PromotionTitle,discounts=discounts,CustomerEmail=CustomerEmail)
    if output =='Item added to cart successfully!':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/home')


@app.route('/recommendation')
def Recommendation():
    if 'username' not in session:
        return redirect('/login')
    return render_template('recommendation.html')


@app.route('/favourites')
def Favourites():
    if 'username' not in session:
        return redirect('/login')
    return render_template('favourites.html')


@app.route('/handle-Add-to-favourite-from-home',methods=['GET','POST'])
def addToFavourite():
    if 'username' not in session:
        return redirect('/login')
    
    menu_title = request.args.get('ItemName')
    Description = request.args.get('Description')
    Price = request.args.get('Price')
    CustomerEmail = session['username'] 
    
    output = DataBase.addToFavourites(menu_title=menu_title,Description=Description,Price=Price,CustomerEmail=CustomerEmail)
    if output =='Item added to cart successfully!':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/home')



@app.route('/discounts')
def discounts():
    if 'username' not in session:
        return redirect('/login')
    data= DataBase.get_active_promotions(current_date=date.today().strftime("%Y-%m-%d"),all=True)
    print(data)
    return render_template('discounts.html',data=data)


@app.route('/cart')
def cart():
    if 'username' not in session:
        return redirect('/login')
    
    dataa = DataBase.get_all_cart(session['username'])
    print(dataa)
    return render_template('cart.html',data=dataa)
  


@app.route('/')
def login_redirect():
    if 'username' in session:
        user = DataBase.EmailCheck(session['username'])
        if user == 'Customer':
            return redirect(url_for('home'))
        elif user == 'Restaurant':
            return redirect(url_for('restaurantHome'))
        else:
            redirect(url_for('login'))
    return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect('/login')
    return render_template('profile.html', username=session['username'])









# resturant



@app.route('/restaurantHome')
def restaurantHome():
    if 'username' not in session:
        return redirect('/login')
    return render_template('restaurantHome.html')







# Admin 

@app.route('/admin')
def admin():
    if 'admin' in session:
        redirect(url_for('adminHome'))
    return redirect(url_for('adminlogin'))


@app.route('/adminHome')
def adminHome():
    if 'admin' not in session:
        return redirect('adminlogin')
    return render_template('adminHome.html',name=DataBase.get_admin_name(session['admin']))

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
    
    return render_template('Adminlogin.html')


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
    return render_template('AddnewAdmin.html')



@app.route('/remove-admin',methods=['GET','POST'])
def removeadmin():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    return render_template('removeAdmin.html',admins = DataBase.get_All_admins())


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
    
    return render_template('allusers.html',users=DataBase.get_all_Customers())





@app.route('/handle-block-user',methods=['GET','POST'])
def handleblockresturant():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    
    id = request.args.get('id')
    
    output = DataBase.blockUser(CustomerID=id,adminMail=session['admin'])
    if output =='':
        flash('User blocked successfully!', 'success')
    else:
        flash(output, 'error')
    
    return redirect('All-Users')


@app.route('/handle-unbloack-user',methods=['GET','POST'])
def handleunblockresturant():
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
    
    return render_template('allresturants.html',resturants=DataBase.get_all_restaurants())





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


@app.route('/handle-unbloack-resturant',methods=['GET','POST'])
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



# Common for all users and resturants

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
            if status == '':
                flash('Customer added successfully','success')
                session['username'] = email
                return redirect(url_for('home'))
            else:
                flash(status,'error')
        elif account_type == 'restaurant':
            status =DataBase.insert_restaurants(email=email,password=password,registration_date=registration_date)
            if status == '':
                flash('Restaurant added successfully','success')
                session['username'] = email
                return redirect(url_for('home'))
            else:
                flash(status,'error')
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
                session['username'] = email
                return redirect(url_for('home'))
            else:
                session['username'] = email
                return redirect(url_for('restaurantHome'))
        else:
            flash(status,'error')
    return render_template('login.html')




if __name__ == '__main__':
    DataBase.create_tables()
    DataBase.insert_default_admin()
    app.run(debug=True, port=5001)
    
