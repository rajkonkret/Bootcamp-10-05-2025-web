from idlelib.autocomplete import TRY_A

from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def index():
    # dla b'color=blue'
    # http://127.0.0.1:5000/?color=blue
    # dla http://127.0.0.1:5000/?color=blue&style=italic
    # b'color=blue&style=italic'
    print(request.query_string)
    # print(request.args['color']) # blue
    # print(request.args['color1']) # exceptions.BadRequestKeyError

    color = "black"
    if 'color' in request.args:
        # print(request.args['color']) # b'color=red'
        color = request.args['color']

    style = 'normal'
    if 'style' in request.args:
        style = request.args['style']

    # return '<h1>Hello World!</h1>'
    return f'<h1 style="color: {color}; font-style:{style};">Hello World!</h1>'


if __name__ == '__main__':
    app.run(debug=True)
