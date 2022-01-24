import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Show and group transactions by symbol
    rows= db.execute("""
        SELECT symbol, SUM(shares) as totalShares
        FROM transactions
        WHERE user_id = :user_id
        GROUP BY symbol
        HAVING totalShares > 0;
        """, user_id=session["user_id"])

    holdings = []
    grand_total = 0
    for row in rows:
        stock = lookup(row["symbol"])
        holdings.append({
            "symbol": stock["symbol"],
            "name": stock["name"],
            "shares": row["totalShares"],
            "price": usd(stock["price"]),
            # usd to display in dollars and display in correct format for dollars
            "total": usd(stock["price"] * row["totalShares"])
        })

       # Execute query to get current balance of user and display this and grand total (balance left + value of current shares)
        grand_total = stock["price"] * row["totalShares"]
    rows = db.execute("SELECT cash FROM users where id=:user_id", user_id=session["user_id"])
    cash = rows[0]["cash"]
    grand_total += cash

    return render_template("index.html", holdings=holdings, cash=usd(cash), grand_total=usd(grand_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

    # Error check for valid symbol and number of shares
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        stock = lookup(symbol)

        if not symbol:
            return apology ("Please provide stock symbol")
        if not lookup(symbol):
            return apology ("Invalid symbol")
        if int(shares) <= 0:
            return apology ("Must be a positive number of shares")

        rows = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
        cash = rows[0]["cash"]

        # calculated new balance
        updated_cash = cash - shares * stock['price']

        # Check for sufficient funds
        if updated_cash < 0:
            return apology("Insufficient funds")

        # Update users total cash in user table following purchase
        db.execute("UPDATE users SET cash=:updated_cash WHERE id=:id",
                    updated_cash=updated_cash,
                    id=session["user_id"])

        # Enter relevant data into transaction table to be used for index screen and transaction history
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
            user_id = session["user_id"],
            symbol = stock["symbol"],
            shares = shares,
            price = stock["price"])
        flash("Bought!")
        return redirect("/")

    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    transactions = db.execute("""
                    SELECT symbol, shares, price, transacted
                    FROM transactions
                    WHERE user_id=:user_id
                    """, user_id= session["user_id"])
    for i in range(len(transactions)):
        transactions[i]["price"] = usd(transactions[i]["price"])
    return render_template("history.html", transactions=transactions)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    #Display form to request a stock quote

    # Lookup stock symbol entered
    if request.method == "POST":
        quote = lookup(request.form.get("stock_symbol"))

    # Check if symbol is valid
        if not quote:
            return apology("Stock could not be found")

    # Display current price of stock
        return render_template("quoted.html", quote=quote)

    # If nothing entered return to quote screen
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username!")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Ensure password confirmation was submitted
        elif not request.form.get("password_confirmation"):
            return apology("must provide password confirmation")

        # Ensure passwords are matching
        elif request.form.get("password") != request.form.get("password_confirmation"):
            return apology("Sorry, password didn't match. Try Again!")

        # Hash password / Store password hash_password
        hashed_password = generate_password_hash(request.form.get("password"))

        # Add user to database
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                username = request.form.get("username"),
                hash = hashed_password)

        if not result:
            return apology("The username is already taken")

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                  username = request.form.get("username"))


        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        # Error check for valid symbol and number of shares
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        stock = lookup(symbol)

        rows = db.execute("""
                SELECT symbol, SUM(shares) as totalShares
                FROM transactions
                WHERE user_id=:user_id
                GROUP BY symbol
                HAVING totalShares > 0;
                """, user_id=session["user_id"])

        # Check user has the required number of shares to sell
        for row in rows:
            if row["symbol"] == symbol:
                if shares > row["totalShares"]:
                    return apology("Insufficient shares")

        # calculated new balance
        rows = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
        cash = rows[0]["cash"]
        updated_cash = cash + shares * stock['price']

        # Update users total cash in user table following purchase
        db.execute("UPDATE users SET cash=:updated_cash WHERE id=:id",
                    updated_cash=updated_cash,
                    id=session["user_id"])

        # Enter relevant data into transaction table to be used for index screen and transaction history
        db.execute("""
            INSERT INTO transactions
                (user_id, symbol, shares, price)
            VALUES (:user_id, :symbol, :shares, :price)
            """,
            user_id = session["user_id"],
            symbol = stock["symbol"],
            shares = -1 * shares,
            price = stock["price"])
        flash("Sold!")
        return redirect("/")

    # Provide a list of owned shares that the user can sell
    else:
        rows= db.execute("""
                SELECT symbol
                FROM transactions
                WHERE user_id=:user_id
                GROUP BY symbol
                HAVING SUM(shares) > 0;
                """, user_id=session["user_id"])
        return render_template("sell.html", symbols= [ row["symbol"] for row in rows ])


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
