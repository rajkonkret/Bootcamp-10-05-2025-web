from datetime import datetime

from flask import Flask
from wtyczka import MojaWtyczka

app = Flask(__name__)
moja_wtyczka = MojaWtyczka(app)


@app.route("/")
def index():
    time_now = datetime.now().strftime("%H:%M:%S")
    print(moja_wtyczka)
    return f"Witaj w mojej aplikacji {time_now}"


if __name__ == '__main__':
    app.run(debug=True)
