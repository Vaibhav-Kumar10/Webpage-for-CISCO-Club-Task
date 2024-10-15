
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