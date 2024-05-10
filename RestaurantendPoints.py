from flask import Blueprint,Flask, render_template, redirect, request, session,flash,url_for,current_app
import DataBase
import helpingFunctions
from datetime import date,datetime
import os
from werkzeug.utils import secure_filename
from socket_events import socketio

Restaurant = Blueprint('Restaurant', __name__)


@Restaurant.route('/chatRes')
def chatRes():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_Restaurant(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    res = DataBase.get_resturant_info(id = session['username'])
    return render_template('restaurant/chat.html',username=res[2])



@Restaurant.route('/restaurantHome')
def restaurantHome():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_Restaurant(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    
    resturantName = DataBase.getResturantName(session['username'])
    
    data = DataBase.get_item_vs_sale(session['username'])
    if len(data):
        Graphans = True
    else:
        Graphans = False
    reviews = DataBase.get_comments_and_ratings(session['username'])
    if len(reviews):
        reviewAns = True
    else:
        reviewAns = False
        
    return render_template('restaurant/Home.html',resturantName=resturantName,sales_data=data,graph=Graphans,reviewAns=reviewAns,review=reviews)

@Restaurant.route('/resturantprofile',methods=['GET','POST'])
def resturantprofile():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_Restaurant(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    data = DataBase.get_resturant_info(id = session['username'])
    if request.method == 'POST':
        nameInput = request.form['nameInput']
        emailInput = request.form['emailInput']
        descriptionInput = request.form['descriptionInput']
        addressInput = request.form['addressInput']
        phoneInput = request.form['phoneInput']
        password = request.form['password-input']
        websiteInput = request.form['websiteInput']
        hoursInput = request.form['hoursInput']
        DataBase.UpdateResturant(name=nameInput,email=emailInput,website=websiteInput,hours=hoursInput,description=descriptionInput,password=password,phone=phoneInput,address=addressInput,id=session['username'])  
        data = DataBase.get_resturant_info(id = session['username'])
        
    return render_template('restaurant/Profile.html',data=data)


@Restaurant.route('/addItem',methods=['GET','POST'])
def addProduct():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not DataBase.is_Restaurant(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    if request.method == 'POST':
        nameInput = request.form['itemName']
        descriptionInput = request.form['description']
        price = request.form['price']
        category_input = request.form['category']
        image_png_file = request.files['imagePng']
        image_jpg_file = request.files['imageJpg']
        
        image_png_file.save('static/images/' + nameInput + '.png')
        image_jpg_file.save('static/images/' + nameInput + '.jpg')
        
        result = DataBase.addItem(ItemName=nameInput,Description=descriptionInput,RestaurantID=session['username'],Price=price,Category=category_input,ImageJPG=nameInput+'.jpg',ImagePNG=nameInput+'.png')
        
        if result == 'Item added successfully!':
            flash(result,'success')
        else:
            flash(result,'error')
    
    return render_template('restaurant/AddProduct.html')
    
@Restaurant.route('/deleteItem',methods=['GET','POST'])
def deleteProduct():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not DataBase.is_Restaurant(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    
    if request.method == 'POST':
        productid = request.form['productid']


        result = DataBase.removeItem(productid,session['username'])
        if result == 'Deleted!':
            flash(result,'success')
        else:
            flash(result,'error')
    
    return render_template('restaurant/DeleteProduct.html')

@Restaurant.route('/updateItem',methods=['GET','POST'])
def updateProduct():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not DataBase.is_Restaurant(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    idRecieved = False
    data=[]
    if request.method == 'POST':
        productid = request.form['productid']
        data = DataBase.get_Item(id=productid,RestaurantID=session['username'])
        if data:
            idRecieved =True
        else:
            flash('You have no item with this id','error')
            idRecieved =False
            
    return render_template('restaurant/UpdateProduct.html',idRecieved=idRecieved,data=data)

@Restaurant.route('/updateItemHandler',methods=['GET','POST'])
def updateProductHandler():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not DataBase.is_Restaurant(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404

    if request.method == 'POST':
        nameInput = request.form['itemName']
        descriptionInput = request.form['description']
        price = request.form['price']
        category_input = request.form['category']
        image_png_file = request.files['imagePng']
        image_jpg_file = request.files['imageJpg']
        menuid = request.form['menuid']
        
        if image_png_file.filename != '':
            image_png_file.save('static/images/' + nameInput + '.png')
            imageNamePNG = nameInput+'.png'
        else:
            imageNamePNG = category_input+'.png'
        if image_jpg_file.filename != '':
            image_jpg_file.save('static/images/' + nameInput + '.jpg')
            imageNameJPG = nameInput+'.jpg'
        else:
            imageNameJPG = category_input+'.jpg'
        
        result = DataBase.updateItem(ItemName=nameInput,Description=descriptionInput,RestaurantID=session['username'],Price=price,Category=category_input,ImageJPG=imageNameJPG,ImagePNG=imageNamePNG,menuid=menuid)
        
        if result == 'Item updated successfully!':
            flash(result,'success')
        else:
            flash(result,'error')
    return redirect('updateItem')    

@Restaurant.route('/allItems')
def allProducts():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not DataBase.is_Restaurant(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    
    data = DataBase.get_Items_ofRestaurant(session['username'])
    
    return render_template('restaurant/allProducts.html',menu=data)

@Restaurant.route('/addPromotion',methods=['GET','POST'])
def addPromotion():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not DataBase.is_Restaurant(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    
    if request.method == 'POST':
        promoName = request.form['promoName']
        menuId = request.form['menuId']
        description = request.form['description']
        discount = request.form['discount']
        startDate = request.form['startDate']
        date_object = datetime.strptime(startDate, '%Y-%m-%d')
        startDate = date_object.strftime('%Y-%m-%d')
        endDate = request.form['endDate']
        date_object = datetime.strptime(endDate, '%Y-%m-%d')
        endDate = date_object.strftime('%Y-%m-%d')
        
        result = DataBase.addpromotion(MenuID=menuId,restaurantid=session['username'],PromotionName=promoName,Description=description,Discount=discount,StartDate=startDate,EndDate=endDate)
        if result == 'Promotion added successfully!':
            flash(result,'success')
        else:
            flash(result,'error')
            
    return render_template('restaurant/AddPromotion.html')

@Restaurant.route('/removePromotion',methods=['GET','POST'])
def removePromotion():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not DataBase.is_Restaurant(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    
    if request.method == 'POST':
        Promotionid = request.form['productid']

        result = DataBase.removePromotion(Promotionid,session['username'])
        if result == 'Deleted!':
            flash(result,'success')
        else:
            flash(result,'error')
    
    return render_template('restaurant/DeletePromotion.html')


@Restaurant.route('/updatePromotion',methods=['GET','POST'])
def updatePromotion():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not DataBase.is_Restaurant(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    
    idRecieved = False
    data=[]
    if request.method == 'POST':
        promotionid = request.form['productid']
        data = DataBase.get_Promotion(id=promotionid,RestaurantID=session['username'])
        idRecieved =True
        if len(data) ==0:
            idRecieved = False
            flash('Cannot access that Promotion','error')
        
        
    return render_template('restaurant/UpdatePromotion.html',idRecieved=idRecieved,data=data)

@Restaurant.route('/updatePromotionHandler',methods=['GET','POST'])
def updatePrmotionHandler():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not DataBase.is_Restaurant(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404

    if request.method == 'POST':
        promoName = request.form['promoName']
        menuId = request.form['menuId']
        description = request.form['description']
        discount = request.form['discount']
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        promotionid = request.form['promotionid']
               
        result = DataBase.updatePromotion(promoName=promoName,menuId=menuId,description=description,Discount=discount,StartDate=startDate,endDate=endDate,promotionid=promotionid,RestaurantID=session['username'])
        
        if result == 'Promotion updated successfully!':
            flash(result,'success')
        else:
            flash(result,'error')
    return redirect('updatePromotion')    

@Restaurant.route('/allPromotions')
def allPromotions():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not DataBase.is_Restaurant(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    
    data = DataBase.get_all_Promotions(RestaurantID=session['username'])
    return render_template('restaurant/allPromotions.html',promotion=data)

@Restaurant.route('/ordersHistory')
def ordersHistory():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not DataBase.is_Restaurant(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    data = DataBase.get_Completed_orders(session['username'])
    return render_template('restaurant/ordersHistory.html',data=data,length=len(data))

@Restaurant.route('/placedOrders',methods=['GET','POST'])
def placedOrders():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not DataBase.is_Restaurant(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    
    if request.method == 'POST':
        status = request.form['status']
        orderid = request.form['orderid']
        result = DataBase.Update_status(status=status,orderID=orderid)
        if result =='Status updated successfully!':
            flash(result,'success')
        else:
            flash(result,'error')
    data = DataBase.get_pending_orders(session['username'])
    return render_template('restaurant/placedOrders.html',data=data,length=len(data))

@Restaurant.route('/aboutusResturant')
def aboutusResturant():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not DataBase.is_Restaurant(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    return render_template('restaurant/aboutusResturant.html')

