from flask import Blueprint,Flask, render_template, redirect, request, session,flash,url_for,current_app
import secrets
import DataBase
import helpingFunctions
from datetime import date,datetime
import os
from werkzeug.utils import secure_filename
import math
User = Blueprint('User', __name__)



@User.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    data = DataBase.get_menu_data(limit=6)
    Pro = DataBase.get_active_promotions(current_date=date.today().strftime("%Y-%m-%d"), limit=2)
    return render_template('user/home.html',menu_data=data,Promotions=Pro)

@User.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
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

@User.route('/handle-Add-to-cart-from-search',methods=['GET','POST'])
def addToCartSearch():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
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

@User.route('/handle-Add-to-cart-from-recommend',methods=['GET','POST'])
def addToCartrecommend():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
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

@User.route('/handle-Add-to-cart-from-favourite',methods=['GET','POST'])
def addToCartfavourite():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
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

@User.route('/handle-Add-to-cart-from-home',methods=['GET','POST'])
def addToCartHome():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
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



@User.route('/handle-Add-to-cart-Promotion-from-home',methods=['GET','POST'])
def addToCartPromotionHome():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    PromotionTitle = request.args.get('PromotionName')
    discounts = request.args.get('discount')
    Customerid = session['username'] 
    
    output = DataBase.addToCartPromotion(PromotionTitle=PromotionTitle,discounts=discounts,Customerid=Customerid)
    if output =='Item added to cart successfully!':
        
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/home')

@User.route('/recommendation',methods=['GET','POST'])
def Recommendation():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
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
            if len(Data) !=0:
                ans = True
            else:
                ans = False
        print(Data)
    return render_template('user/recommendation.html',menu=Data,item_names=helpingFunctions.get_all_item_name(),query=query,ans=ans,name=input)

@User.route('/favourites')
def Favourites():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    data =DataBase.get_favourite_data(session['username'])
    return render_template('user/favourites.html',menu=data,result=len(data))

@User.route('/handle-Add-to-favourite-from-home',methods=['GET','POST'])
def addToFavouriteHome():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
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

@User.route('/handle-remove-to-favourite-from-favourites',methods=['GET','POST'])
def removeFromFavourite():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
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

@User.route('/handle-Add-to-favourite-from-search',methods=['GET','POST'])
def addToFavouriteSearch():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
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

@User.route('/handle-Add-to-favourite-from-recommend',methods=['GET','POST'])
def addToFavouriterecommend():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
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

@User.route('/handle-Add-to-fav-Promotion-from-discount',methods=['GET','POST'])
def addToFavouriteDiscount():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    Promotion = request.args.get('PromotionName')
    Customerid = session['username'] 
    
    output = DataBase.addToFavourites(PromotionName=Promotion,Customerid=Customerid)
    if output =='Item added to cart successfully!' or output == 'Item Removed from Favourites':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/discounts')

@User.route('/handle-Add-to-cart-from-discount',methods=['GET','POST'])
def addToCartDiscount():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    PromotionTitle = request.args.get('PromotionName')
    Customerid = session['username'] 
    print(PromotionTitle)
    output = DataBase.addToCartPromotion(PromotionTitle=PromotionTitle,discounts=0,Customerid=Customerid)
    if output =='Item added to cart successfully!':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/discounts')

@User.route('/discounts')
def discounts():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    data= DataBase.get_active_promotions(current_date=date.today().strftime("%Y-%m-%d"),all=True,png=True)
    print(data)
    return render_template('user/discounts.html',data=data,result=len(data))

@User.route('/cart')
def cart():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    dataa = DataBase.get_all_cart(session['username'])
    # cursor.execute('''SELECT m.ItemName, m.Price, p.Discount, m.ImagePNG, c.Instructions ,m.Menuid , c.quantity
    total = 0
    total_with_discount = 0
    for item in dataa:
        original_price = item['OriginalPrice']
        discounted_price = item['DiscountedPrice']  # corrected variable name
        quantity = item['quantity']
    
        total += original_price * quantity
    
        total_with_discount += discounted_price * quantity
        
    return render_template('user/cart.html',data=dataa,total=math.ceil(total),total_with_dicount=math.ceil(total_with_discount),dicount=math.ceil(total-total_with_discount))
  
@User.route('/handle-remove-from-cart',methods=['GET','POST'])
def removefromCart():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    menuid = request.args.get('menuid')
    Customerid = session['username'] 
    output = DataBase.removeFromcart(menuid=menuid,Customerid=Customerid)
    if output =='Deleted!':
        flash('Item deleted from cart', 'success')
    else:
        flash(output, 'error')
    return redirect('/cart') 

@User.route('/handle-instruction-from-cart',methods=['GET','POST'])
def instructionfromCart():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    menuid = request.args.get('menuid')
    instruction = request.args.get('instruction')
    quantity = request.args.get('quantity')
    Customerid = session['username'] 
    print(quantity,menuid,Customerid)
    output = DataBase.UpdateFromcart(menuid=menuid,Customerid=Customerid,instruction=instruction,quantity=quantity)
    if output =='item updated!':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/cart') 

@User.route('/handle-order-from-cart',methods=['GET','POST'])
def orderfromCart():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    Customerid = session['username'] 
    Type = request.args.get('type')
    output = DataBase.placeOrder(customerid=Customerid,date=date.today().strftime("%Y-%m-%d"),Type=Type)
    print(output)
    if output =='Order placed successfully!':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/cart') 
 
@User.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
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
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], imageName))
        else:
            if data[5]!='default.jpg':
                imageName = data[5]
            else:
                imageName = 'default.jpg'
        DataBase.UpdateCustomer(name=name,email=email,password=password,phone=phone,imageName=imageName,address=address,id=session['username'])  
        data = DataBase.get_customer_info(id = session['username'])
    print(data)
    return render_template('user/profile.html',data=data)

@User.route('/trackorders')
def trackOrders():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    data = DataBase.get_order_details(customer_id=session['username'])
    return render_template('user/trackorders.html',order_details=data,dataLength=len(data))

@User.route('/add-review',methods=['POST','GET'])
def addReview():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    if request.method == 'POST':
        rating = request.form['rating']
        comment = request.form['comment']
        order_id = request.form['order_id']
        DataBase.UpdateRating(Customerid=session['username'],orderid=order_id, rating=rating,comment=comment)
        
    
    return redirect('trackorders')

@User.route('/restaurants',methods=['GET','POST'])
def AllRestaurants():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    data =DataBase.get_active_restaurants()
    return render_template('user/restaurants.html',data=data,length=len(data))

@User.route('/restaurantDetail')
def restaurantDetails():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    restaurant_id = request.args.get('restaurant_id')
    items = DataBase.get_Items_ofRestaurant(restaurant_id)
    restaurant = DataBase.get_a_restaurant(restaurant_id)
    return render_template('user/restaurant_detail.html',items=items,itemslength=len(items),res_data=restaurant)

@User.route('/handle-Add-to-cart-from-resDet',methods=['GET','POST'])
def addToCartresDet():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    menu_title = request.args.get('ItemName')
    Description = request.args.get('Description')
    Price = request.args.get('Price')
    resid = request.args.get('resid')
    Customerid = session['username'] 
    print(menu_title,Description,Price,Customerid)
    output = DataBase.addToCart(menu_title=menu_title,Description=Description,Price=Price,Customerid=Customerid)
    print(output)
    if output =='Item added to cart successfully!':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/restaurantDetail?restaurant_id=' + str(resid))


@User.route('/handle-Add-to-favourite-from-resDet',methods=['GET','POST'])
def addToFavouriteresDet():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    menu_title = request.args.get('ItemName')
    Description = request.args.get('Description')
    resid = request.args.get('resid')
    Price = request.args.get('Price')
    Customerid = session['username'] 
    
    output = DataBase.addToFavourites(menu_title=menu_title,Description=Description,Price=Price,Customerid=Customerid)
    if output =='Item added to cart successfully!' or output == 'Item Removed from Favourites':
        flash(output, 'success')
    else:
        flash(output, 'error')
    return redirect('/restaurantDetail?restaurant_id=' + str(resid))


@User.route('/chat',methods=['GET','POST'])
def chat():
    if 'username' not in session:
        return redirect('/login')
    if not DataBase.is_customer(session['username'],session['email'],session['password']):
        return render_template('404.html'), 404
    
    restaurant_id = request.args.get('restaurant_id')
    
    data = DataBase.get_a_restaurant(restaurant_id)
    cus = DataBase.get_customer_info(session['username'])
    return render_template('user/chat.html', res_data=data,username=cus[2])
    