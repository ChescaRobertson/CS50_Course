import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

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

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///budget.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show overall balance, spending in categories, savings, balance and transactions, predicted balance and actual balance for month"""
    # TO DO

    if request.method == "POST":
        # Add inputted income into cashflow database table
        db.execute(""" 
                    INSERT INTO income 
                    (user_id, income, inptdate) 
                    VALUES (:user_id, :income, :inptdate)
                    """,
                    user_id = session["user_id"],
                    income = request.form.get("income"),
                    inptdate = request.form.get("date"),
                    )
        return redirect("/")

            
    if request.method == "GET":

        # Display monthly income, expenses and balance as well as predicted expenses and balance and overall savings
        # Select and display current monthly income
        monthly_income = db.execute(""" SELECT Sum(income) FROM income
                                        WHERE user_id=:user_id
                                        AND strftime('%m', inptdate) = strftime('%m', 'now')""",
                                        user_id =session["user_id"]
                                        )
        monthly_income = monthly_income[0].get('Sum(income)')
        if monthly_income == None:
            monthly_income = 0

        # Select and display current monthly expenses
        monthly_expenses = db.execute(""" SELECT Sum(amount) FROM expenses
                                        WHERE user_id=:user_id
                                        AND strftime('%m', inptdate) = strftime('%m', 'now')
                                        """,
                                        user_id =session["user_id"]
                                        )
        monthly_expenses = monthly_expenses[0].get('Sum(amount)')

        # Calculate current monthly balance

        monthly_balance = monthly_income - monthly_expenses

        # Calculate predicted expenses for the month based on average of all other months
        # NEED TO FIX THIS (CONSIDER GETTING RID??)
        predicted_expenses =  db.execute(""" SELECT AVG(month_amount)
                                            FROM (
                                            SELECT SUM(amount) AS month_amount
                                            FROM expenses
                                            WHERE user_id=:user_id
                                            AND strftime('%y', '%m', inptdate) <= strftime('%y', '%m', 'now')
                                            )""",
                                            user_id = session["user_id"])
        predicted_expenses = predicted_expenses[0].get('Avg(month_amount)')
        if predicted_expenses == None:
            predicted_expenses = 0
        
        # Calculate predicted balance for end of current month based on current income and predicted expenses
        predicted_balance = monthly_income - predicted_expenses

        # Select and display current total savings
        savings = db.execute(""" SELECT Sum(amount)
                                FROM savings
                                WHERE user_id=:user_id""",
                                user_id =session["user_id"])
        savings = savings[0].get('Sum(amount)')
        if savings == None:
            savings = 0

        return render_template("index.html", monthly_expenses=monthly_expenses, monthly_income=monthly_income, monthly_balance=monthly_balance, predicted_expenses=predicted_expenses, predicted_balance=predicted_balance, savings=savings)

@app.route("/transactions", methods=["GET", "POST"])
@login_required
def transactions():
    """Show expenses, categories and allow adding and removing categories"""

    if request.method == "POST":
        # Add new expense into transactions table
        db.execute("""
            INSERT INTO expenses
            (user_id, category, description, amount, inptdate)
            VALUES (:user_id, :category, :description, :amount, :inptdate)
            """,
            user_id = session["user_id"],
            category = request.form.get("category"),
            description = request.form.get("description"),
            amount = request.form.get("amount"),
            inptdate = request.form.get("date"),
            )
        return redirect("/transactions")

    else:
        # Display transactions
        rows = db.execute("SELECT name FROM categories WHERE user_id=:user_id", user_id=session["user_id"])

        expenses = db.execute ("SELECT category, description, amount, inptdate FROM expenses WHERE user_id=:user_id", user_id=session["user_id"])
        total_expenses = db.execute("SELECT Sum(amount) FROM expenses WHERE user_id= :user_id", user_id= session["user_id"])
        return render_template("transactions.html", expenses=expenses, names = [ row["name"] for row in rows])


@app.route("/categories", methods=["GET", "POST"])
@login_required
def categories():
    """Place to view and add categories"""

    if request.method == "POST":

        # Add new category into categories table
        db.execute("""
            INSERT INTO categories
            (user_id, name, description, type)
            VALUES (:user_id, :name, :description, :type)
            """,
            user_id = session["user_id"],
            name = request.form.get("name"),
            description = request.form.get("description"),
            type = request.form.get("type")
            )
        return redirect("/categories")

    if request.method == "GET":
        # Display current categories
        categories = db.execute ("SELECT name, description, type FROM categories WHERE user_id=:user_id", user_id=session["user_id"])
        return render_template("categories.html", categories=categories)

@app.route("/predictions", methods=["GET"])
@login_required
def predicted():
    """Show predicted balance at end of month"""
    # TO DO
    

@app.route("/savings", methods=["GET", "POST"])
@login_required
def savings():
    """Show savings, categories, add more savings"""
    # TO DO
    if request.method == "POST":
        # Add new expense into transactions table
        db.execute("""
            INSERT INTO savings
            (user_id, category, description, amount, inptdate)
            VALUES (:user_id, :category, :description, :amount, :inptdate)
            """,
            user_id = session["user_id"],
            category = request.form.get("category"),
            description = request.form.get("description"),
            amount = request.form.get("amount"),
            inptdate = request.form.get("date"),
            )
        return redirect("/savings")

    else:
        # Display savings
        rows = db.execute("SELECT name FROM categories WHERE user_id=:user_id", user_id=session["user_id"])

        savings = db.execute ("SELECT category, description, amount, inptdate FROM savings WHERE user_id=:user_id", user_id=session["user_id"])
        total_savings = db.execute("SELECT Sum(amount) FROM savings WHERE user_id= :user_id", user_id= session["user_id"])
        return render_template("savings.html", savings=savings, names = [ row["name"] for row in rows])



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
        #return redirect("/")

        # CHANGE THIS LATER, TO TEST EXPENSES
        return redirect ("/")

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
        # return redirect("/transactions")



    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")