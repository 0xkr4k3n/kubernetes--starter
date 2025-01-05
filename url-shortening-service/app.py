from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import hashlib

app = Flask(__name__)

# IMPORTANT: Use port 3306 internally (the container's MySQL port) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://urluser:urlpass@db:3306/url_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), unique=True, nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)

def initialize_database():
    with app.app_context():
        db.create_all()

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data['longUrl']
    
    existing_url = URL.query.filter_by(long_url=long_url).first()
    if existing_url:
        return jsonify({'shortUrl': f'http://localhost:5000/{existing_url.short_url}'}), 200

    short_url = hashlib.md5(long_url.encode()).hexdigest()[:6]
    new_url = URL(long_url=long_url, short_url=short_url)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({'shortUrl': f'http://localhost:5000/{short_url}'}), 201


if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, host='0.0.0.0')
