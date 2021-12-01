from flask import Flask, render_template
# from pymongo import MongoClient

# client = MongoClient()
# db = client.Playlister
# playlists = db.playlists

app = Flask(__name__)

@app.route('/')
def index():
    """Return homepage."""
    return 'Hello to the world!'

if __name__ == '__main__':
    app.run(debug=True)