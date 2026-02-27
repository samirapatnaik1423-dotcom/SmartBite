# SmartBite
SmartBite – Food Ordering & Cart Management System

SmartBite is a full-stack food ordering web application built using Python, Flask, HTML, CSS, and SQLite. It allows users to sign up, log in, browse Indian food items, add them to a cart, place orders, and view order history.

### Features:
Authentication,
User Signup (Username & Password),
User Login,
Session-based authentication,
Logout functionality,
Duplicate username prevention,
Menu System,
30+ Indian Veg & Non-Veg food items

### Categories:
Breakfast, Main Course, Starters, Breads, Desserts, Beverages

Food images for each item,
Clean styled menu display,
Cart System,
Add to Cart (POST method),
Quantity management,
Subtotal & Total price calculation,
Session-based cart storage,
Order Processing,
Confirm Order

## Stores:
Username.
Ordered Items,
Total Amount,
Date & Time,
Cart clears after order,
Order success page,
Order History,
Users can view previous orders,
Displays order details and total amount

### Tech Stack:
#### Frontend:
HTML5,
CSS3

#### Backend:
Python,
Flask,
SQLite,
Sessions,
GET & POST methods

#### Project Structure:
SmartBite/ <br>
app.py <br>
database.db <br>
templates/ <br>
login.html <br>
signup.html <br>
menu.html <br>
cart.html <br>
success.html <br>
static/ <br>
style.css <br>
images/ <br>

#### Database Schema:
users  
id (Primary Key)
username (Unique)
password
menu
id (Primary Key)
name
category
price
image
orders
id (Primary Key)
username
items
total
datetime

### How to Run:
Install Flask
pip install flask
**Run the app:**
python app.py

**Open in browser:**
http://127.0.0.1:5000

## Developed By:
Behera Samira Patnaik <br>
BTech 3rd Year Student <br>
Full-Stack Mini Project
