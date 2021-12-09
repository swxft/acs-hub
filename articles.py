from flask import Blueprint, render_template

article = Blueprint("article", __name__)

@article.route("/article")
# @article.route("/")
def articles_new():
    return render_template('articles_new.html', article=None, title='New Article')