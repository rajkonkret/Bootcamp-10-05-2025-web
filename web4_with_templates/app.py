from flask import Flask, render_template, url_for, request

app = Flask(__name__)


@app.route("/")
def index():
    return "This is index"


# http://127.0.0.1:5000/exchange
# jinja2 - silnik uzywany w renderowaniu templatek z kodu pythonowego
# 127.0.0.1 - - [03/Aug/2025 12:32:47] "POST /exchange HTTP/1.1" 200 -
@app.route("/exchange", methods=['GET', 'POST'])
def exchange():
    if request.method == "GET":
        return render_template('exchange.html')
    else:
        currency = "EUR"
        if "currency" in request.form:
            currency = request.form['currency']

        amount = 250
        if 'amount' in request.form:
            amount = request.form['amount']

        return render_template('exchange_results.html', currency=currency, amount=amount)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
