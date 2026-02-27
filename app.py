from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = "smartbite_secret_key"


# ---------------- DATABASE SETUP ----------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # USERS TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # MENU TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        price REAL,
        image TEXT
    )
    """)

    # ORDERS TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        items TEXT,
        total REAL,
        datetime TEXT
    )
    """)

    # INSERT MENU ITEMS IF EMPTY
    c.execute("SELECT * FROM menu")
    if not c.fetchall():
        menu_items = [

            # Breakfast
            ("Idli (2 pcs)", "Breakfast", 40, "idli.jpg"),
            ("Plain Dosa", "Breakfast", 60, "dosa.jpg"),
            ("Masala Dosa", "Breakfast", 80, "masala_dosa.jpg"),
            ("Vada (2 pcs)", "Breakfast", 50, "vada.jpg"),
            ("Uttapam", "Breakfast", 70, "uttapam.jpg"),
            ("Upma", "Breakfast", 50, "upma.jpg"),
            ("Aloo Paratha", "Breakfast", 70, "aloo_paratha.jpg"),
            ("Chole Bhature", "Breakfast", 120, "chole_bhature.jpg"),
            ("Poha", "Breakfast", 45, "poha.jpg"),
            ("Bread Omelette", "Breakfast", 60, "bread_omelette.jpg"),

            # Main Course
            ("Veg Biryani", "Main Course", 150, "veg_biryani.jpg"),
            ("Chicken Biryani", "Main Course", 200, "chicken_biryani.jpg"),
            ("Paneer Butter Masala", "Main Course", 180, "paneer_butter_masala.jpg"),
            ("Butter Naan", "Main Course", 40, "butter_naan.jpg"),
            ("Rajma Chawal", "Main Course", 130, "rajma_chawal.jpg"),
            ("Dal Tadka", "Main Course", 120, "dal_tadka.jpg"),
            ("Veg Fried Rice", "Main Course", 140, "veg_fried_rice.jpg"),
            ("Chicken Curry", "Main Course", 190, "chicken_curry.jpg"),
            ("Matar Paneer", "Main Course", 160, "matar_paneer.jpg"),
            ("Roti (2 pcs)", "Main Course", 30, "roti.jpg"),

            # Beverages
            ("Filter Coffee", "Beverages", 30, "coffee.jpg"),
            ("Sweet Lassi", "Beverages", 50, "lassi.jpg"),
            ("Masala Chai", "Beverages", 20, "chai.jpg"),
            ("Badam Milk", "Beverages", 60, "badam_milk.jpg"),
            ("Buttermilk", "Beverages", 25, "buttermilk.jpg"),

            # Desserts
            ("Gulab Jamun (2 pcs)", "Desserts", 50, "gulab_jamun.jpg"),
            ("Rasgulla (2 pcs)", "Desserts", 50, "rasgulla.jpg"),
            ("Kaju Katli", "Desserts", 80, "kaju_katli.jpg"),
            ("Ice Cream (Vanilla)", "Desserts", 60, "icecream.jpg"),
            ("Gajar Halwa", "Desserts", 90, "gajar_halwa.jpg"),
        ]

        c.executemany("INSERT INTO menu (name, category, price, image) VALUES (?, ?, ?, ?)", menu_items)

    conn.commit()
    conn.close()


init_db()


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            return render_template("signup.html", error="All fields required!")

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=?", (username,))
        if c.fetchone():
            conn.close()
            return render_template("signup.html", error="Username already exists!")

        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, password))
        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("signup.html")


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["username"] = username
            session["cart"] = {}
            return redirect(url_for("menu"))
        else:
            return render_template("login.html", error="Invalid Credentials!")

    return render_template("login.html")


# ---------------- MENU (Search + Category Filter) ----------------
@app.route("/menu")
def menu():
    if "username" not in session:
        return redirect(url_for("login"))

    search_query = request.args.get("search")
    category = request.args.get("category")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    query = "SELECT * FROM menu WHERE 1=1"
    params = []

    if search_query:
        query += " AND name LIKE ?"
        params.append('%' + search_query + '%')

    if category:
        query += " AND category = ?"
        params.append(category)

    c.execute(query, params)
    items = c.fetchall()
    conn.close()

    return render_template("menu.html", items=items)


# ---------------- ADD TO CART ----------------
@app.route("/add_to_cart/<int:item_id>", methods=["POST"])
def add_to_cart(item_id):
    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM menu WHERE id=?", (item_id,))
    item = c.fetchone()
    conn.close()

    cart = session.get("cart", {})

    if str(item_id) in cart:
        cart[str(item_id)]["quantity"] += 1
    else:
        cart[str(item_id)] = {
            "name": item[1],
            "price": item[3],
            "quantity": 1
        }

    session["cart"] = cart
    return redirect(url_for("menu"))


# ---------------- CART ----------------
@app.route("/cart")
def cart():
    if "username" not in session:
        return redirect(url_for("login"))

    cart = session.get("cart", {})
    total = sum(item["price"] * item["quantity"] for item in cart.values())

    return render_template("cart.html", cart=cart, total=total)


# ---------------- CONFIRM ORDER ----------------
@app.route("/confirm", methods=["POST"])
def confirm():
    if "username" not in session:
        return redirect(url_for("login"))

    cart = session.get("cart", {})
    if not cart:
        return redirect(url_for("menu"))

    total = sum(item["price"] * item["quantity"] for item in cart.values())
    items_str = ", ".join([f"{v['name']} x {v['quantity']}" for v in cart.values()])

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO orders (username, items, total, datetime) VALUES (?, ?, ?, ?)",
              (session["username"], items_str, total, str(datetime.datetime.now())))
    conn.commit()
    conn.close()

    session["cart"] = {}
    return render_template("success.html", total=total)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)