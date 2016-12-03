from flask import Flask
from framework.router import Router
from views.home import HomeView

app = Flask(__name__)
router = Router(app)

router.get('/', HomeView.index)

if __name__ == '__main__':
    app.run()
