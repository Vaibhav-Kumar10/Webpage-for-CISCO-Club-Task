from flask import Flask, render_template, url_for, redirect, flash, request, session
import mysql.connector as sql
import re

app = Flask(__name__)
app.secret_key = "secret key"

fn = ""
ln = ""
em = ""
pwd = ""


# Database connection function
def get_db_connection():
    connection = sql.connect(
        host="localhost", database="CISCO", user="root", password="manu"
    )
    return connection


# Initialize the database and create users table
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        create table IF NOT EXISTS records (
            fname varchar(50) not null,
            lname varchar(50) not null,
            email varchar(50) not null unique,
            password varchar(50) not null
        )
    """
    )
    conn.commit()
    conn.close()


# Home route
@app.route("/")
def d():
    return render_template("signup.html")


@app.route("/home")
def home():
    return render_template("home.html")


# Dashboard route (protected page)
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        flash("username")
        return render_template("dashboard.html")
    else:
        return redirect(url_for("login"))


# Blog route
@app.route("/blog")
def blog():
    return render_template("blog.html")


# Services route
@app.route("/services")
def services():
    return render_template("services.html")


# About route
@app.route("/about")
def about():
    return render_template("about.html")


# Sign-up route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    msg = ""
    global fn, ln, em, pwd
    if request.method == "POST":

        d = request.form
        for key, value in d.items():
            if key == "fname":
                fn = value
            if key == "lname":
                ln = value
            if key == "email":
                em = value
            if key == "password":
                pwd = value

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            "select * from records where email='{}'".format(em)
            record = cursor.fetchone()

            if record:
                msg = "record already exists !"
                flash(msg)
                return redirect(url_for("signup"))

            elif not re.match(r"[A-Za-z]+", fn):
                msg = "First name must contain only characters!"
                flash(msg, "danger")
                return redirect(url_for("signup"))

            elif not re.match(r"[A-Za-z]+", ln):
                msg = "Last name must contain only characters!"
                flash(msg, "danger")
                return redirect(url_for("signup"))

            elif not fn or not ln or not em or not pwd:
                msg = "Please fill out the form !"
                flash(msg, "danger")
                return redirect(url_for("signup"))

            else:
                query = "insert into records Values('{}','{}','{}','{}')".format(
                    fn, ln, em, pwd
                )
                cursor.execute(query)
                conn.commit()
                msg = "You have successfully registered !"
                flash(msg, "danger")
                return redirect(url_for("home"))

        # except sql.IntegrityError:
        except Exception:
            msg = "Username already exists. Please try a different one."
            flash(msg, "danger")
            return redirect(url_for("signup"))

    msg = "Please fill out the form !"
    flash(msg, "danger")
    return render_template("signup.html")


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    global em, pwd
    if request.method == "POST":

        d = request.form
        for key, value in d.items():
            if key == "email":
                em = value
            if key == "password":
                pwd = value

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "select * from records where email='{}' and password='{}'".format(em, pwd)
        )
        record = cursor.fetchone()

        if record:
            session["loggedin"] = True
            session["username"] = record[1]

            msg = "Logged in successfully !"
            flash(msg, "danger")
            return redirect(url_for("dashboard"))

        elif not em:
            msg = "Email should not be empty !"
            # messages.append(msg)
            flash(msg, "danger")
            return redirect(url_for("login"))

        elif not pwd:
            msg = "Password should not be empty !"
            # messages.append(msg)
            flash(msg, "danger")
            return redirect(url_for("login"))

        else:
            msg = "Incorrect email / password !. Try Again"
            # messages.append(msg)
            flash(msg, "danger")
            return redirect(url_for("login"))

    msg = "Please fill out the form !"
    flash(msg, "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("username", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    init_db()  # Ensure the database is set up
    app.run(debug=True)
