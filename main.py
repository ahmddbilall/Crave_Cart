from flask import Flask, render_template, redirect, request, session,flash,url_for
import secrets
import DataBase
import helpingFunctions
from datetime import date

secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.secret_key = secret_key
currentUser = ''

        
        
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')




@app.route('/search')
def search():
    if 'username' not in session:
        return redirect('/login')
    return render_template('search.html')


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

@app.route('/discounts')
def discounts():
    if 'username' not in session:
        return redirect('/login')
    return render_template('discounts.html')


@app.route('/cart')
def cart():
    if 'username' not in session:
        return redirect('/login')
    return render_template('cart.html')
  



@app.route('/')
def login_redirect():
    if 'username' in session:
        user = DataBase.EmailCheck(session['username'])
        if user == 'User':
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











#a seperate view for resturant



@app.route('/restaurantHome')
def restaurantHome():
    if 'username' not in session:
        return redirect('/login')
    return render_template('restaurantHome.html')




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
            flash('User with this email already exists', 'error')
            return redirect(url_for('signup'))

        registration_date = date.today().strftime("%Y-%m-%d")
        if account_type == 'user':
            status =DataBase.insert_user(email=email,password=password,registration_date=registration_date)
            if status == '':
                flash('User added successfully','success')
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
    
        if status == 'User' or status == 'Restaurant':
            currentUser = status
            if (currentUser == 'User'):
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
    app.run(debug=True, port=5001)
    
