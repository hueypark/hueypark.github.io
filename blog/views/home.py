from flask import render_template


class HomeView:
    @staticmethod
    def index():
        return render_template('index.html')
