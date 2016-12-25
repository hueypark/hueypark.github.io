import os
from flask import render_template


POST_DIR = os.getcwd() + '/posts'


class PostView:
    @classmethod
    def posts(cls):
        titles = []
        for root, _, files in os.walk(POST_DIR):
            for file in files:
                post_file = os.path.join(root, file)
                titles.append(
                    {
                        'name': cls.__get_title(post_file),
                        'url': 'posts/' + file.lower().replace('.md', '')
                    })

        return render_template('posts.html', titles=titles)

    @classmethod
    def post(cls, post_id):
        post_file = POST_DIR + '/' + post_id + '.md'
        return cls.__get_content(post_file)

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

    @staticmethod
    def __get_content(post_file):
        content = ''
        with open(post_file, 'r', encoding='utf-8') as f:
            is_content_start = False
            for line in f.readlines():
                if line == '\n':
                    is_content_start = True
                    continue
                elif not is_content_start:
                    continue

                content += line

        return content
