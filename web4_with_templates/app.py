from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return "This is index"

# http://127.0.0.1:5000/exchange
# jinja2 - silnik uzywany w renderowaniu templatek z kodu pythonowego
# 127.0.0.1 - - [03/Aug/2025 12:32:47] "POST /exchange HTTP/1.1" 200 -
@app.route("/exchange", methods=['GET', 'POST'])
def exchange():
     return render_template('exchange.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
