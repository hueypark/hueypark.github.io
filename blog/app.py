from flask import Flask
from framework.router import Router
from views.post import PostView


app = Flask(__name__)
router = Router(app)

router.get('/', PostView.posts)
router.get('/posts', PostView.posts)
router.get('/posts/<post_id>', PostView.post)

if __name__ == '__main__':
    app.run(debug=True)
