import re
from flask import Flask, render_template, request, redirect, url_for, json
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
# from articles import article
""" 
Useful Commands:
source venv/bin/activate

source deactivate

pip3 freeze > requirements.txt

export FLASK_ENV=development; flask run

http://9444-73-237-162-244.ngrok.io || localhost:5000

./ngrok http 5000
copy <this_link> -> http://localhost:5000


This link only works when ngrok is in use

"""

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"


mongo = PyMongo(app)
client = MongoClient()
db = client.ACSHub
articles = db.articles
suggestions = db.suggestions



@app.route('/')
def articles_index():
    return render_template('articles_index.html', articles=articles.find())


@app.route('/webhook', methods=['POST'])
def webhook():
    response = request.json
    # response = json.dumps(request.json, indent=2)
    # for item in response:
    #     print(item)
    # print(f"title is: {response.get('title')}")
    print(response["object"]["title"])
    print(response["object"]["details"])
    return response


# New Article Form Route ----------------------
@app.route('/articles/new')
def articles_new():
    return render_template('articles_new.html', article=None, title='New Article')


# Create a New Playlist ---------------------------
@app.route('/articles', methods=['POST'])
def articles_submit():
    article = {
        'title': request.form.get('title'),
        'body': request.form.get('body'),
        'author': request.form.get('author'),
    }
    articles.insert_one(article) # add the new playlist to the db


    return render_template('articles_show.html', article=article)

# Show 1 Playlist + Actions you can take on it ---------------------------
@app.route('/articles/<article_id>')
def articles_show(article_id):
    article = articles.find_one({'_id': ObjectId(article_id)})
    # playlist_comments = comments.find({'playlist_id': ObjectId(playlist_id)})
    return render_template('articles_show.html', article=article) #, comments=playlist_comments)
    # return render_template('playlists_show.html', playlist=playlist, playlists=playlists.find())



# Form to Edit an Article  ------------
@app.route('/articles/<article_id>/edit')
def articles_edit(article_id):
    article = articles.find_one({'_id': ObjectId(article_id)})
    return render_template('articles_edit.html', article=article)



# Submit the Edit of a Article ------------
@app.route('/articles/<article_id>', methods=['POST'])
def articles_update(article_id):
    updated_article = {
        'title': request.form.get('title'),
        'body': request.form.get('body'),
        'author': request.form.get('author'),
    }
    articles.update_one(
        {'_id': ObjectId(article_id)},
        {'$set': updated_article}
    )
    return redirect(url_for('articles_show', article_id=article_id))



# Delete an Article 
@app.route('/articles/<article_id>/delete', methods=['POST'])
def articles_delete(article_id):
    articles.delete_one({'_id': ObjectId(article_id)})
    return redirect(url_for('articles_index'))


# Create a New Suggestion ---------------------------
@app.route('/suggestion', methods=['POST'])
def suggestion_submit():
    suggestion = {
        'anon_upvote': request.form.get('title'),
        'anon_downvote': request.form.get('body'),
        #canny_post_id
        #canny_post_title
        #canny_post_body
        #canny_post_url
    }
    suggestions.insert_one(suggestion) # add the new playlist to the db
    """
    show all suggestions
        title
        body
    button to upvote (number of upvotes)
    button to downvote (number of downvotes)

    """
    return render_template('articles_show.html', article=article)


# Add Upvote of a Suggestion ------------
@app.route('/suggestions/<suggestion_id>', methods=['POST'])
def suggestions_update(suggestion_id):
    updated_suggestion = {
        'upvote': request.form.get('title'),
        'downvote': request.form.get('body'),
        'author': request.form.get('author'),
    }
    articles.update_one(
        {'_id': ObjectId(article_id)},
        {'$set': updated_article}
    )
    suggestions.update_one(suggestion), {'$inc': {'upvote': 1}} # have only one, so update they
    return redirect(url_for('articles_show', article_id=article_id))


# Delete a Suggestion
@app.route('/suggestion/<suggestion_id>/delete', methods=['POST'])
def suggestion_delete(suggestion_id):
    suggestions.delete_one({'_id': ObjectId(suggestion_id)})
    return redirect(url_for('suggestion_index'))




@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(500)
def something_went_wrong(e):
    # note that we set the 404 status explicitly
    return render_template('500.html'), 500



if __name__ == '__main__':
    app.run(debug=True)