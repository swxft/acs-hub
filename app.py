from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
""" 
Useful Commands:
source venv/bin/activate

source deactivate

pip3 freeze > requirements.txt

export FLASK_ENV=development; flask run

http://127.0.0.1:5000/ || localhost:5000
"""

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"


mongo = PyMongo(app)
client = MongoClient()
db = client.ACSHub
articles = db.articles



@app.route('/')
def articles_index():
    """Show all articles."""
    return render_template('base.html', articles=articles.find())



# Home Route ----------------------
@app.route('/')
def playlists_index():
    return render_template('playlists_index.html', playlists=playlists.find())


# New Article Form Route ----------------------
@app.route('/articles/new')
def playlists_new():
    return render_template('articles_new.html', article=None, title='New Article')


# Create a New Playlist ---------------------------
@app.route('/articles', methods=['POST'])
def playlists_submit():
    article = {
        'title': request.form.get('author'),
        'author': request.form.get('author'),
        'body': request.form.get('description'),
    }
    articles.insert_one(article) # add the new playlist to the db


    return render_template('articles_show.html', article=article)

# # Show 1 Playlist + Actions you can take on it ---------------------------
# @app.route('/articles/<article_id>')
# def playlists_show(playlist_id):
#     playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
#     playlist_comments = comments.find({'playlist_id': ObjectId(playlist_id)})
#     return render_template('playlists_show.html', playlist=playlist, comments=playlist_comments)
#     # return render_template('playlists_show.html', playlist=playlist, playlists=playlists.find())



# # Form to Edit a Playlist ------------
# @app.route('/articles/<article_id>/edit')
# def playlists_edit(playlist_id):
#     playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
#     return render_template('playlists_edit.html', playlist=playlist)



# # Submit the Edit of a Playlist ------------
# @app.route('/articles/<article_id>', methods=['POST'])
# def playlists_update(playlist_id):
#     video_ids = request.form.get('video_ids').split()
#     videos = video_url_creator(video_ids)
#     updated_playlist = {
#         'title': request.form.get('title'),
#         'description': request.form.get('description'),
#         'videos': videos,
#         'video_ids': video_ids
#     }
#     playlists.update_one(
#         {'_id': ObjectId(playlist_id)},
#         {'$set': updated_playlist}
#     )
#     return redirect(url_for('playlists_show', playlist_id=playlist_id))



# # Delete a Playlist 
# @app.route('/articles/<article_id>/delete', methods=['POST'])
# def playlists_delete(playlist_id):
#     playlists.delete_one({'_id': ObjectId(playlist_id)})
#     return redirect(url_for('playlists_index'))




@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(500)
def something_went_wrong(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(debug=True)