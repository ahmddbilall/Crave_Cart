from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'Restaurants'

    RestaurantID = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
    Description = Column(String(255))
    Address = Column(String(255))
    PhoneNumber = Column(String(20))
    Email = Column(String(100))
    Website = Column(String(255))

class MenuItem(Base):
    __tablename__ = 'MenuItems'

    MenuItemID = Column(Integer, primary_key=True)
    RestaurantID = Column(Integer, ForeignKey('Restaurants.RestaurantID'))
    Name = Column(String(100), nullable=False)
    Description = Column(String(255))
    Price = Column(Float, nullable=False)
    SpecialOffer = Column(String(255))
    restaurant = relationship('Restaurant', back_populates='menu_items')

Restaurant.menu_items = relationship('MenuItem', back_populates='restaurant')

class User(Base):
    __tablename__ = 'Users'

    UserID = Column(Integer, primary_key=True)
    Username = Column(String(100), nullable=False)
    Email = Column(String(100), nullable=False)
    Password = Column(String(255), nullable=False)
    RegistrationDate = Column(DateTime, default=datetime.now)
    LoyaltyPoints = Column(Integer, default=0)

class Order(Base):
    __tablename__ = 'Orders'

    OrderID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'))
    OrderDate = Column(DateTime, default=datetime.now)
    TotalAmount = Column(Float, nullable=False)
    DeliveryAddress = Column(String(255))
    OrderType = Column(String(20), nullable=False)  # Delivery, Pickup, Dine-In
    OrderStatus = Column(String(20), nullable=False)  # Pending, In Progress, Completed, Cancelled
    user = relationship('User', back_populates='orders')

User.orders = relationship('Order', back_populates='user')

class OrderItem(Base):
    __tablename__ = 'OrderItems'

    OrderItemID = Column(Integer, primary_key=True)
    OrderID = Column(Integer, ForeignKey('Orders.OrderID'))
    MenuItemID = Column(Integer, ForeignKey('MenuItems.MenuItemID'))
    Quantity = Column(Integer, nullable=False)
    SpecialRequests = Column(String(255))
    order = relationship('Order', back_populates='order_items')
    menu_item = relationship('MenuItem', back_populates='order_items')

Order.order_items = relationship('OrderItem', back_populates='order')
MenuItem.order_items = relationship('OrderItem', back_populates='menu_item')

class Review(Base):
    __tablename__ = 'Reviews'

    ReviewID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'))
    RestaurantID = Column(Integer, ForeignKey('Restaurants.RestaurantID'))
    Rating = Column(Integer, nullable=False)
    Comment = Column(String(255))
    ReviewDate = Column(DateTime, default=datetime.now)

class Favorite(Base):
    __tablename__ = 'Favorites'

    UserID = Column(Integer, ForeignKey('Users.UserID'), primary_key=True)
    MenuItemID = Column(Integer, ForeignKey('MenuItems.MenuItemID'), primary_key=True)

class Promotion(Base):
    __tablename__ = 'Promotions'

    PromotionID = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
    Description = Column(String(255))
    Discount = Column(Float, nullable=False)
    Active = Column(Boolean, nullable=False)

class Admin(Base):
    __tablename__ = 'Admins'

    AdminID = Column(Integer, primary_key=True)
    Username = Column(String(100), nullable=False)
    Email = Column(String(100), nullable=False)
    Password = Column(String(255), nullable=False)

class SupportRequest(Base):
    __tablename__ = 'SupportRequests'

    RequestID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'))
    RequestType = Column(String(50), nullable=False)  # Inquiry, Issue, Technical Support
    RequestDetails = Column(String(255))
    RequestDate = Column(DateTime, default=datetime.now)

class Recommendation(Base):
    __tablename__ = 'Recommendations'

    RecommendationID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'))
    MenuItemID = Column(Integer, ForeignKey('MenuItems.MenuItemID'))
    Score = Column(Float)
    
class LocationSuggestion(Base):
    __tablename__ = 'LocationSuggestions'

    LocationSuggestionID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'))
    RestaurantID = Column(Integer, ForeignKey('Restaurants.RestaurantID'))
    Score = Column(Float)

engine = create_engine('sqlite:///your_database.db')  # Replace 'your_database.db' with your database URI
Base.metadata.create_all(engine)
