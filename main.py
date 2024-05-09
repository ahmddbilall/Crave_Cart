from flask import Flask, render_template, redirect, request, session,flash,url_for
import secrets
import DataBase
import helpingFunctions
from datetime import date,datetime
import os
from werkzeug.utils import secure_filename
from AdminendPoints import Admin
from RestaurantendPoints import Restaurant
from userEndpoints import User

secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.secret_key = secret_key
app.config['UPLOAD_FOLDER'] = 'static/images'

app.register_blueprint(Admin)
app.register_blueprint(Restaurant)
app.register_blueprint(User)
  
  
@app.route('/')
def login_redirect():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route('/Aboutus')
def aboutus():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('aboutus.html')

@app.route('/logout')
def logout():
    if session.get('username'):
        session.pop('username', None)
    else:
        session.pop('admin', None)
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
                session['email'] = email
                session['password'] = password
                return redirect(url_for('User.home'))
        elif account_type == 'restaurant':
            status =DataBase.insert_restaurants(email=email,password=password,registration_date=registration_date)
            if isinstance(status, str):
                flash(status,'error')
            else:
                flash('Restaurant added successfully','success')
                session['username'] = status
                session['email'] = email
                session['password'] = password
                return redirect(url_for('Restaurant.restaurantHome'))
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
                session['email'] = email
                session['password'] = password
                return redirect(url_for('User.home'))
            else:
                session['username'] = DataBase.get_restaurants_id(email,password)
                session['email'] = email
                session['password'] = password
                return redirect(url_for('Restaurant.restaurantHome'))
        else:
            flash(status,'error')
    return render_template('login.html')




if __name__ == '__main__':
    DataBase.create_tables()
    DataBase.insert_default_admin()
    app.run(debug=True, port=5001)
    
