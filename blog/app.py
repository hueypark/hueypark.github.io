from flask import Flask
from framework.router import Router
from views.home import HomeView
from views.post import PostView


app = Flask(__name__)
router = Router(app)

router.get('/', HomeView.index)
router.get('/posts', PostView.posts)

if __name__ == '__main__':
    app.run(debug=True)
