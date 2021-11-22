from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

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


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    Simbolo = db.execute("SELECT * FROM transaciotns WHERE user_id = :ID", ID=session['user_id'])
    resultado = db.execute("SELECT cash FROM users WHERE ID = :ID", ID=session['user_id'])
    Total_dinero = float(resultado[0]['cash'])
    Gran_total = Total_dinero

    for k in Simbolo:
        Symbolo = str(k["Simbolo"])
        Acciones = int(float(k["Acciones"]))
        quote = lookup(Symbolo)
        Precio = float(quote['price'])

        total_del_valor_acciones = float(Precio * Acciones)

        Gran_total += total_del_valor_acciones

    return render_template("Index.html", Symbolo=Simbolo, cash=Total_dinero, total_del_valor_acciones=Gran_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session['user_id'])
        s = request.form.get("symbol")
        l = int(request.form.get("shares"))
        d = lookup(s)
        if not d:
            return apology("proporcione un simbolo valido")
        h = float(d['price'])
        t = (l * h)
        valor = cash[0]['cash'] - t
        f = datetime.now().strftime("%y/%m/%d, %H:%M:%S")

        if l < 0:
            return apology("proporcione un numero valido")

        m = db.execute("INSERT INTO transaciotns(Simbolo, Nombre, Acciones, Precio, Total, fectransaction, user_id) VALUES(:symbol, :name, :shares, :price, :total, :fecha, :id_user)",
                       symbol=s, name=d['name'], shares=l, price=h, total=t, fecha=f, id_user=session['user_id'])

        db.execute("UPDATE users SET cash = :valor WHERE id = :user_id", user_id=session['user_id'], valor=valor)

        db.execute("INSERT INTO Historial(Simbolo, Acciones, Precio, Transaccion, user_id) VALUES (:symbol, :shares, :price, :fecha, :id_user)",
                   symbol=s, shares=l, price=h, fecha=f, id_user=int(session['user_id']))

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    resultados = db.execute("SELECT * FROM Historial WHERE user_id = :ID", ID=session['user_id'])

    return render_template("history.html", Symbolo=resultados)


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
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("debe proporcionar un simbolo")

        resultado = lookup(request.form.get("symbol"))

        if not resultado:
            return apology("simbolo invalido")

        return render_template("quoted.html", nombre=resultado["name"], precio=resultado["price"], simbolo=resultado["symbol"])
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("debe proporcionar un nombre de usuario")

    # ejecuta la contraseña primaria
        elif not request.form.get("password"):
            return apology("debe proporcionar una contraseña")

        # ejecuta la confirmacion de contraseña
        elif not request.form.get("confirmation"):
            return apology("debe proporcionar una confirmacion")

        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("la contraseña es incorrecta")

        rows = db.execute("INSERT INTO users(username, hash) VALUES(:username, :hash)",
                          username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        if rows is None:
            return apology("lo sentimos ha ocurrido un error al ingresar")

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        session["user_id"] = rows[0]["id"]

        return redirect(url_for("index"))

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    h = db.execute("SELECT Simbolo FROM transaciotns WHERE user_id = :ID", ID=session['user_id'])
    if request.method == "POST":
        p = int(request.form.get("shares"))
        s = request.form.get("Symbol")
        if s is None:
            return apology("rellene el campo")

        if g is None:
            return apology("rellene el campo")
        r = db.execute("SELECT * FROM transaciotns WHERE user_id = :ID", ID=session['user_id'])
        g = lookup(s)
        f = p * g['price']
        o = datetime.now().strftime("%y/%m/%d, %H:%M:%S")

        if not r[0]['Acciones'] < p:
            return apology("lo sentimos no cuenta con suficientes acciones")

        db.execute("UPDATE users SET cash = :f WHERE id = :user_id", user_id=session['user_id'], f=f)

        db.execute("INSERT INTO Historial(Simbolo, Acciones, Precio, Transaccion, user_id) VALUES(:symbol, :shares, :price, :fecha, :id_user)",
                   symbol=s, shares=p*-1, price=f, fecha=o, id_user=session['user_id'])
        return redirect(url_for("index"))

    else:
        return render_template("sell.html", globalo=h)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)