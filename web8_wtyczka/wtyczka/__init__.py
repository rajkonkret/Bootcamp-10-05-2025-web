from flask import Flask

class MojaWtyczka:
    def __init__(self, app: Flask):
        self.app = app
        self.initialization()

    def initialization(self):

        @self.app.route("/moja-funkcja")
        def moja_funkcja():
            return "Witaj z wtyczki"