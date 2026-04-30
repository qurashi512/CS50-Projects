import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd
 
# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# ==================== INDEX ====================

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # جيب كل الأسهم اللي عند الـ user
    stocks = db.execute("""
        SELECT symbol, SUM(shares) AS total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, user_id)

    # جيب الكاش الحالي
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # احسب القيمة الإجمالية
    total_value = cash
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["value"] = stock["price"] * stock["total_shares"]
        total_value += stock["value"]

    return render_template("index.html",
                           stocks=stocks,
                           cash=cash,
                           total_value=total_value)


# ==================== REGISTER ====================

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # التحقق من الإدخال
        if not username:
            return apology("must provide username", 400)
        if not password:
            return apology("must provide password", 400)
        if not confirmation:
            return apology("must confirm password", 400)
        if password != confirmation:
            return apology("passwords do not match", 400)

        # حفظ الـ user في الـ DB
        try:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username,
                generate_password_hash(password)
            )
        except ValueError:
            return apology("username already exists", 400)

        # تسجيل دخول تلقائي
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]

        flash("Registered successfully! 🎉")
        return redirect("/")

    return render_template("register.html")


# ==================== LOGIN ====================

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        if not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    return render_template("login.html")


# ==================== LOGOUT ====================
@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


# ==================== QUOTE ====================

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", stock=stock)

    return render_template("quote.html")


# ==================== BUY ====================

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # التحقق من الإدخال
        if not symbol:
            return apology("must provide symbol", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol", 400)

        try:
            shares = int(shares)
            if shares <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return apology("shares must be a positive integer", 400)

        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        cost = stock["price"] * shares

        # التحقق من وجود كاش كافي
        if cash < cost:
            return apology("not enough cash", 400)

        # خصم الكاش وتسجيل المعاملة
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, user_id)
        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?)
        """, user_id, stock["symbol"], shares, stock["price"])

        flash(f"Bought {shares} share(s) of {stock['symbol']}! ✅")
        return redirect("/")

    return render_template("buy.html")


# ==================== SELL ====================

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    # جيب الأسهم المتاحة للبيع
    stocks = db.execute("""
        SELECT symbol, SUM(shares) AS total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, user_id)

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # التحقق من الإدخال
        if not symbol:
            return apology("must select a symbol", 400)

        try:
            shares = int(shares)
            if shares <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return apology("shares must be a positive integer", 400)

        # التحقق من وجود أسهم كافية
        owned = db.execute("""
            SELECT SUM(shares) AS total FROM transactions
            WHERE user_id = ? AND symbol = ?
            GROUP BY symbol
        """, user_id, symbol)

        if not owned or owned[0]["total"] < shares:
            return apology("not enough shares", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol", 400)

        revenue = stock["price"] * shares

        # إضافة الكاش وتسجيل المعاملة (shares سالبة = بيع)
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", revenue, user_id)
        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?)
        """, user_id, symbol, -shares, stock["price"])

        flash(f"Sold {shares} share(s) of {symbol}! 💰")
        return redirect("/")

    return render_template("sell.html", stocks=stocks)


# ==================== HISTORY ====================

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute("""
        SELECT symbol, shares, price, transacted
        FROM transactions
        WHERE user_id = ?
        ORDER BY transacted DESC
    """, user_id)

    return render_template("history.html", transactions=transactions)


# ==================== PERSONAL TOUCH 1: Add Cash ====================

@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Allow user to add cash to account"""
    if request.method == "POST":
        amount = request.form.get("amount")

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return apology("invalid amount", 400)

        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            amount,
            session["user_id"]
        )

        flash(f"Added ${amount:,.2f} to your account! 💵")
        return redirect("/")

    return render_template("add_cash.html")


# ==================== PERSONAL TOUCH 2: Change Password ====================

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allow user to change password"""
    if request.method == "POST":
        current = request.form.get("current_password")
        new = request.form.get("new_password")
        confirm = request.form.get("confirmation")

        if not current or not new or not confirm:
            return apology("must fill all fields", 400)

        if new != confirm:
            return apology("new passwords do not match", 400)

        # التحقق من الباسورد الحالي
        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]
        if not check_password_hash(user["hash"], current):
            return apology("current password is incorrect", 400)

        # تحديث الباسورد
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            generate_password_hash(new),
            session["user_id"]
        )

        flash("Password changed successfully! 🔐")
        return redirect("/")

    return render_template("change_password.html")
