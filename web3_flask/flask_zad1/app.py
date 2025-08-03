from flask import Flask

# pip install Flask

app = Flask(__name__)

# http://127.0.0.1:5000 - 5000 standartowy port dla Flaska
@app.route("/")
def index():
    return "Hello World!!!"

# 127.0.0.1:5000/about
@app.route("/about")
def about():
    a = 10
    b = 1
    # return "<h1>We are programers</h1>"
    return f"<h1>We are programers {a / b}</h1>"

# http://127.0.0.1:5000/error
@app.route("/error")
def error():
    a = 10
    b = 0
    return f"<h1>We are programers {a / b}</h1>"

# http://127.0.0.1:5000/cantor/usd/100
# @app.route("/cantor/<currency>/<amount>")
# gdy dodamy int, flask nie widzi url dla takiej operacji:
# 127.0.0.1 - - [03/Aug/2025 10:07:53] "GET /cantor/eur/sto HTTP/1.1" 404 -
@app.route("/cantor/<string:currency>/<int:amount>")
def cantor(currency, amount): # nazwy zmiennych odpowiadaja nazwą parametrów w url
    message = f"<h1>You selected {currency} and {amount}</h1>"
    return message

if __name__ == '__main__':
    app.run(debug=True)
# port standardowy 5000
