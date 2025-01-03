from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import hashlib
from flask_cors import CORS


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), unique=True, nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)

# Initialize the database explicitly
def initialize_database():
    with app.app_context():
        db.create_all()

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data['longUrl']
    
    # Check if the URL already exists
    existing_url = URL.query.filter_by(long_url=long_url).first()
    if existing_url:
        return jsonify({'shortUrl': f'http://localhost:5000/{existing_url.short_url}'}), 200

    # Create a unique short URL by hashing the long URL
    short_url = hashlib.md5(long_url.encode()).hexdigest()[:6]  # Take first 6 characters of MD5 hash

    # Save to the database
    new_url = URL(long_url=long_url, short_url=short_url)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({'shortUrl': f'http://localhost:5000/{short_url}'}), 201

@app.route('/<short_url>')
def redirect_to_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first_or_404()
    return jsonify({'redirectUrl': url.long_url})

if __name__ == '__main__':
    initialize_database()  # Call the database initialization
    app.run(debug=True, host='0.0.0.0')
