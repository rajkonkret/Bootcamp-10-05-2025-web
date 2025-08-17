from flask import Flask, render_template, url_for, request, flash, g, redirect, session
import sqlite3

import random
import string
import hashlib
import binascii

app_info = {
    'db_file': 'data/cantor.db'
}

app = Flask(__name__)
# dodajemy secret_key  aby komunikacja flash wykonałą sie w bezpieczny sposób
app.config['SECRET_KEY'] = "KluczTrudnyDoZlamania123!!!"


def get_db():
    if not hasattr(g, 'sqlite_db'):
        conn = sqlite3.connect(app_info['db_file'])
        conn.row_factory = sqlite3.Row  # dostaniemy dane w postaci słownika
        g.sqlite_db = conn

    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


class Currency:
    def __init__(self, code, name, flag):
        self.code = code
        self.name = name
        self.flag = flag

    def __repr__(self):
        return f'<Currency {self.code}>'


class CantorOffer:

    def __init__(self):
        self.currencies = []
        self.denied_codes = []

    def load_offer(self):
        """
        Ładuje dane do sytemu
        :return:
        """
        self.currencies.append(Currency('USD', "Dollar", 'currencies/dollar.png'))
        self.currencies.append(Currency('EUR', "Euro", 'currencies/euro.jpg'))
        self.currencies.append(Currency('HUF', "Forint", 'currencies/huf.jpg'))
        self.currencies.append(Currency('PLN', "Zloty", 'currencies/zloty.jpg'))
        self.currencies.append(Currency('GBP', "Funt Angielski", 'currencies/gbp.png'))
        self.denied_codes.append('USD')

    def get_by_code(self, code):
        """
        Zwraca obiekt klasy Currency na podstawie kodu waluty
        :param code: kod waluty, którą chcemy wyszukać
        :return:
        """
        for currency in self.currencies:
            if currency.code == code:
                return currency
        return Currency('unknown', 'unknown', 'kantor.png')


class UserPass:

    def __init__(self, user="", password=""):
        self.user = user
        self.password = password
        self.email = ""
        self.is_valid = False
        self.is_admin = False

    # bcrypt
    # os.urandom(60)
    def hash_password(self):
        os_urandom_static = b'\xee\x8b\x9c\xe6n\x96\xa9\xf5@\x99\x9c\xf3\xbf\xf1\x03\x86sr\x05\xcf\xa7\xac\xcf\xb2H\xfe\x7f\x10\x14\x9f%5\xde\xe5\xbd\xaef\x9d\xcd\xf4\xc9Be\xf9\x04\xf9\x1c}\xf9\x8a|\xe4\x92\xe1\xdb\xff~R\x0e\xb1'
        salt = hashlib.sha256(os_urandom_static).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf=8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def verify_password(self, stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf=8'), salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

    def get_random_user_password(self):
        random_user = ''.join(random.choice(string.ascii_lowercase) for i in range(3))
        self.user = random_user

        password_characters = string.ascii_letters  # + string.digits + string.punctations
        random_password = ''.join(random.choice(password_characters) for i in range(3))
        self.password = random_password

    def login_user(self):

        db = get_db()
        sql_statement = 'SELECT id, name, email, password, is_active, is_admin from users where name=?'
        # cur = db.execute(sql_statement, [self.user])
        cur = db.execute(sql_statement, (self.user,))
        user_record = cur.fetchone()  # jako słownik

        if user_record != None and self.verify_password(user_record['password'], self.password):
            return user_record
        else:
            self.user = None
            self.password = None
            return None


@app.route("/login", methods=['GET', 'POST'])
def login():
    # login = UserPass(session.get('user'))

    if request.method == "GET":
        return render_template('login.html', active_menu="login")
    else:
        user_name = '' if "user_name" not in request.form else request.form['user_name']
        user_pass = '' if "user_pass" not in request.form else request.form['user_pass']

        login = UserPass(user_name, user_pass)
        login_record = login.login_user()

        if login_record != None:
            session['user'] = user_name
            flash(f"Logon succesfull, welcome {user_name}")
            return redirect(url_for('index'))
        else:
            flash("Login failed, try again")
            return render_template('login.html', active_menu="login")


@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user', None)
        flash("Ypu are logged out")
    return redirect(url_for('login'))


@app.route("/init_app")
def init_app():
    db = get_db()
    sql_statement = "select count(*) as cnt from users where is_active and is_admin;"
    cur = db.execute(sql_statement)
    active_admins = cur.fetchone()

    if active_admins != None and active_admins['cnt'] > 0:
        flash("Application is already set-up. Nothing to do.")
        return redirect(url_for('index'))

    # tworzymy admina gdy ie ma jeszcze w systemie
    user_pass = UserPass()
    user_pass.get_random_user_password()
    db.execute("""
    INSERT INTO users(name, email, password, is_active, is_admin)
    VALUES (?,?,?,True,True);""",
               (user_pass.user, "radek@radek.pl", user_pass.hash_password()))
    db.commit()

    # User cim with password QRg has been created.
    flash(f"User {user_pass.user} with password {user_pass.password} has been created.")
    return redirect(url_for('index'))


@app.route("/")
def index():
    # return "This is index"
    return render_template('index.html', active_menu='home')


# http://127.0.0.1:5000/exchange
# jinja2 - silnik uzywany w renderowaniu templatek z kodu pythonowego
# 127.0.0.1 - - [03/Aug/2025 12:32:47] "POST /exchange HTTP/1.1" 200 -
@app.route("/exchange", methods=['GET', 'POST'])
def exchange():
    offer = CantorOffer()
    offer.load_offer()

    if request.method == "GET":
        return render_template('exchange.html', active_menu='exchange', offer=offer)
    else:
        currency = "EUR"
        if "currency" in request.form:
            currency = request.form['currency']

        amount = 250
        if 'amount' in request.form:
            amount = request.form['amount']

        if currency in offer.denied_codes:
            flash(f"The currency {currency} cannot be accepted")
        elif offer.get_by_code(currency) == "unknown":
            flash("The selected currency is unknown and cannot be accepted")
        else:
            db = get_db()
            sql_command = "INSERT INTO transactions(currency, amount, user) VALUES (?, ?, ?)"
            db.execute(sql_command, (currency, amount, 'admin'))
            db.commit()
            flash(f"Request to exchange {currency} was accepted")

        return render_template('exchange_results.html',
                               active_menu='exchange',
                               currency=currency,
                               amount=amount,
                               currency_info=offer.get_by_code(currency))


@app.route('/history')
def history():
    db = get_db()
    sql_command = 'SELECT id, currency, amount FROM transactions;'
    cur = db.execute(sql_command)
    transactions = cur.fetchall()  # dostaniemy liste transakcji z bazy

    return render_template('history.html', active_menu='history', transactions=transactions)


@app.route('/delete_transaction/<int:transaction_id>')
def delete_transaction(transaction_id):
    db = get_db()
    sql_statement = 'DELETE FROM transactions WHERE id = ?'
    db.execute(sql_statement, (transaction_id,))
    db.commit()

    return redirect(url_for('history'))


@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    offer = CantorOffer()
    offer.load_offer()
    db = get_db()

    if request.method == "GET":
        sql_statement = "SELECT id, currency, amount FROM transactions WHERE id=?"
        cur = db.execute(sql_statement, (transaction_id,))
        transaction = cur.fetchone()  # pobranie jedego rekordu

        if transaction == None:
            flash("No such transaction!")
            return redirect(url_for('history'))
        else:
            return render_template('edit_transaction.html', transaction=transaction,
                                   offer=offer, active_menu='history')
    else:
        currency = "EUR"
        if "currency" in request.form:
            currency = request.form['currency']

        amount = 250
        if 'amount' in request.form:
            amount = request.form['amount']

        if currency in offer.denied_codes:
            flash(f"The currency {currency} cannot be accepted")
        elif offer.get_by_code(currency) == "unknown":
            flash("The selected currency is unknown and cannot be accepted")
        else:
            db = get_db()
            sql_command = """
            UPDATE transactions SET
            currency=?,
            amount=?,
            user=?
            WHERE id=?;
            """
            db.execute(sql_command, (currency, amount, 'admin', transaction_id))
            db.commit()
            flash(f"Transaction was updated!")

        return redirect(url_for('history'))


@app.route('/users')
def users():
    return "not implemented"


@app.route('/user_status_change/<action>/<user_name>')
def user_status_change(action, user_name):
    return "not implemented"


@app.route('/edit_user/<user_name>', methods=['GET', 'POST'])
def edit_user():
    return "not implemented"


@app.route('/user_delete/<user_name>')
def delete_user(user_name):
    return "not implemented"


@app.route("/new_user", methods=['GET', 'POST'])
def new_user():
    return "not implemented"


if __name__ == '__main__':
    # app.run(debug=True, port=5000)
    app.run(debug=True, port=5005)
