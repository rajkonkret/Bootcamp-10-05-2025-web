import os

from flask import Flask, request, url_for, redirect

app = Flask(__name__)


# url_for('exchange') - podajemy nazwę metody a nie url
@app.route("/")
def index():
    menu = f'''
    Go <a href="{url_for('exchange')}">here</a> to exchange money<br>
    To exchange 50 SEK go <a href="{url_for('cantor', currency='SEK', amount=50)}">here</a>
    <img src="{url_for('static', filename="1.png")}"><br>
    <img src="{url_for('static', filename="currencies/euro.jpg")}"><br>
    {url_for('static', filename="currencies/euro.jpg")}<br>
    {os.path.join(app.static_folder, 'currencies/euro.jpg')}
'''
    return f'<h1>Hello World!</h1><br>{menu}'


# @app.route("/")
# def index():
#     # dla b'color=blue'
#     # http://127.0.0.1:5000/?color=blue
#     # dla http://127.0.0.1:5000/?color=blue&style=italic
#     # b'color=blue&style=italic'
#     print(request.query_string)
#     # print(request.args['color']) # blue
#     # print(request.args['color1']) # exceptions.BadRequestKeyError
#
#     color = "black"
#     if 'color' in request.args:
#         # print(request.args['color']) # b'color=red'
#         color = request.args['color']
#
#     style = 'normal'
#     if 'style' in request.args:
#         style = request.args['style']
#
#     for p in request.args:
#         print(p, request.args[p])
#         # color blue
#         # style italic
#
#     # http://127.0.0.1:5000/?color=red
#     # http://127.0.0.1:5000/?color=blue&style=italic
#     # http://127.0.0.1:5000/?color=blue&style=italic">Hacked<
#     # color blue
#     # style italic">Hacked<
#     # return '<h1>Hello World!</h1>'
#     #  http://127.0.0.1:5000/?color=red&style=italic;%22%3EHacked%3Ch1%20style=%22font-style:italic
#     return f'<h1 style="color: {color}; font-style:{style};">Hello World!</h1>'


@app.route("/cantor/<string:currency>/<int:amount>")
def cantor(currency, amount):  # nazwy zmiennych odpowiadaja nazwą parametrów w url
    message = f"<h1>You selected {currency} and {amount}</h1>"
    return message


# http://127.0.0.1:5000/exchange
# https://flask.palletsprojects.com/en/stable/api/#flask.request
@app.route("/exchange", methods=['GET', 'POST'])
def exchange():
    # <form id="exchange_form" action="/exchange_process" method="POST">
    # <form id="exchange_form" action="/exchange" method="POST">
    print(request.method)

    if request.method == 'GET':
        body = f"""
        <form id="exchange_form" action="{url_for('exchange')}" method="POST">
        <label for="currency">Currency</label>
        <input type="text" id="currency" name="currency" value="EUR"><br>
        <label for="amount">Amount</label>
        <input type="text" id="amount" name="amount" value="100"><br>
        <input type="submit" value="Send">
        </form>
        """
        return body
    else:
        currency = "EUR"
        if "currency" in request.form:
            currency = request.form['currency']

        amount = 250
        if 'amount' in request.form:
            amount = request.form['amount']

        body = f"You want to exchange {amount} {currency}"
        # return body
        # return redirect(url_for('index')) # przekierowanie do funkcji index()
        return redirect(url_for('cantor', currency=currency, amount=amount))


@app.route("/exchange_process", methods=['POST'])
def exchange_process():
    currency = "EUR"
    if "currency" in request.form:
        currency = request.form['currency']

    amount = 250
    if 'amount' in request.form:
        amount = request.form['amount']

    body = f"You want to exchange {amount} {currency}"
    return body


if __name__ == '__main__':
    app.run(debug=True)
