from flask import Flask


class Router:
    def __init__(self, app: Flask):
        self.__app = app

    def get(self, url, view):
        self.__app.add_url_rule(url, view.__qualname__, view, methods=['GET'])
