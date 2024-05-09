from flask import Blueprint,Flask, render_template, redirect, request, session,flash,url_for
import DataBase
import helpingFunctions
from datetime import date,datetime
import os
from werkzeug.utils import secure_filename

Admin = Blueprint('Admin', __name__)





@Admin.route('/aboutusAdmin')
def aboutusAdmin():
    if 'admin' not in session:
        return redirect(url_for('Admin.adminlogin'))
    
    return render_template('admin/aboutusAdmin.html')



@Admin.route('/adminHome')
def adminHome():
    if 'admin' not in session:
        return redirect('adminlogin')
    return render_template('admin/adminHome.html',name=DataBase.get_admin_name(session['admin']))

@Admin.route('/adminlogin',methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        status = DataBase.login_check_Admin(email=email,password=password)
        if status == 'admin':
            session['admin'] = email
            return redirect(url_for('Admin.adminHome'))  
        else:
            flash(status,'error')
    
    return render_template('admin/Adminlogin.html')

@Admin.route('/Add-new-admin',methods=['GET','POST'])
def AddNewadmin():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        if email == 'bilalahmad@gmail.com':
            flash('This email cannot be used','error')
        else:
            status = DataBase.Add_new_admin(email=email,password=password,name=name)
    
            if status == '':
                flash(name + ' added as admin','success')
            else:
                flash(status,'error')
    return render_template('admin/AddnewAdmin.html')

@Admin.route('/remove-admin',methods=['GET','POST'])
def removeadmin():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    return render_template('admin/removeAdmin.html',admins = DataBase.get_All_admins())

@Admin.route('/handle-remove-admin',methods=['GET','POST'])
def handleremoveadmin():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    print('i am here in handle remove admin')
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

@Admin.route('/All-Users')
def AllUsers():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    return render_template('admin/allusers.html',users=DataBase.get_all_Customers())

@Admin.route('/handle-block-user',methods=['GET','POST'])
def handleblockuser():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    
    id = request.args.get('id')
    print('user id to block',id)
    
    output = DataBase.blockUser(CustomerID=id,adminMail=session['admin'])
    print(output)
    if output:
        flash('User blocked successfully!', 'success')
    else:
        flash(output, 'error')
    
    return redirect('All-Users')

@Admin.route('/handle-unblock-user',methods=['GET','POST'])
def handleunblockuser():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    
    id = request.args.get('id')
    
    print(id)
    output = DataBase.unblockUser(CustomerID=id)
    print(output)
    if output:
        flash('User unblocked successfully!', 'success')
    else:
        flash(output, 'error')
    
    return redirect('All-Users')

@Admin.route('/All-Resturants')
def AllResturants():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    return render_template('admin/allresturants.html',resturants=DataBase.get_all_restaurants())

@Admin.route('/handle-block-resturant',methods=['GET','POST'])
def handleblockresturant():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    
    id = request.args.get('id')
    
    output = DataBase.blockResturant(resturantID=id,adminMail=session['admin'])
    if output:
        flash('Resturant blocked successfully!', 'success')
    else:
        flash(output, 'error')
    
    return redirect('All-Resturants')

@Admin.route('/handle-unblock-resturant',methods=['GET','POST'])
def handleunblockresturant():
    if 'admin' not in session:
        return redirect('adminlogin')
    
    
    id = request.args.get('id')
    output = DataBase.unblockResturant(resturantID=id)
    if output:
        flash('Resturant unblocked successfully!', 'success')
    else:
        flash(output, 'error')
    
    return redirect('All-Resturants')
