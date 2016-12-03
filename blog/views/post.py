import os
from flask import render_template


class PostView:
    @classmethod
    def posts(cls):
        posts_dir = os.getcwd() + '/posts'

        titles = []
        for root, _, files in os.walk(posts_dir):
            for file in files:
                post_file = os.path.join(root, file)
                titles.append(
                    {
                        'name': cls.__get_title(post_file),
                        'url': file.lower().replace('.md', '')
                    })

        return render_template('posts.html', titles=titles)

    @staticmethod
    def __get_title(post_file):
        with open(post_file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                data = line.split(':')
                if data[0] == 'title':
                    title = data[1]
                    title = title.replace('\n', '')
                    if title[0] == ' ':
                        title = title[1:]
                    return title
