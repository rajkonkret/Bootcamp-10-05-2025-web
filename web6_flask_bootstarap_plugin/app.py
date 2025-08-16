from flask import flash, render_template, Flask
# uninstall flask-bootstrap
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
