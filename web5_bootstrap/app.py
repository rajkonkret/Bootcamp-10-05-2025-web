from flask import Flask, render_template, url_for, request, flash, g
import sqlite3

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


@app.route("/")
def index():
    # return "This is index"
    return render_template('index.html')


# http://127.0.0.1:5000/exchange
# jinja2 - silnik uzywany w renderowaniu templatek z kodu pythonowego
# 127.0.0.1 - - [03/Aug/2025 12:32:47] "POST /exchange HTTP/1.1" 200 -
@app.route("/exchange", methods=['GET', 'POST'])
def exchange():
    offer = CantorOffer()
    offer.load_offer()

    if request.method == "GET":
        return render_template('exchange.html', offer=offer)
    else:
        currency = "EUR"
        if "currency" in request.form:
            currency = request.form['currency']

        if currency in offer.denied_codes:
            flash(f"The currency {currency} cannot be accepted")
        elif offer.get_by_code(currency) == "unknown":
            flash("The selected currency is unknown and cannot be accepted")
        else:
            flash(f"Request to exchange {currency} was accepted")

        amount = 250
        if 'amount' in request.form:
            amount = request.form['amount']

        return render_template('exchange_results.html',
                               currency=currency,
                               amount=amount,
                               currency_info=offer.get_by_code(currency))


if __name__ == '__main__':
    # app.run(debug=True, port=5000)
    app.run(debug=True, port=5005)
