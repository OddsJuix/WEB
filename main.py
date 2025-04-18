import os
from flask import Flask, render_template, send_from_directory, request, jsonify, redirect, url_for
from models import db, Subscriber, Video, MemeTemplate, CreatedMeme, BananaScore, Feedback, SiteVisit, EasterEggFound
import json
from datetime import datetime

app = Flask(__name__)
# Ensure DATABASE_URL is set and properly formatted for SQLAlchemy
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "moxxievr_secret_bananas"

print(f"Database URL: {database_url}")

# Initialize the database with the app
db.init_app(app)

# Create all tables in the database
with app.app_context():
    db.create_all()
    
    # Check if we need to add initial meme templates
    if MemeTemplate.query.count() == 0:
        templates = [
            MemeTemplate(name="Angry Gorilla", emoji="🦍"),
            MemeTemplate(name="Surprised Gorilla", emoji="🙉"),
            MemeTemplate(name="Dancing Gorilla", emoji="🙈"),
            MemeTemplate(name="Banana Gorilla", emoji="🍌"),
            MemeTemplate(name="Space Gorilla", emoji="🚀"),
        ]
        db.session.add_all(templates)
        db.session.commit()
    
    # Check if we need to add initial videos
    if Video.query.count() == 0:
        videos = [
            Video(
                title="Gorilla Tag Adventures",
                youtube_id="dQw4w9WgXcQ",
                description="Join MoxxieVR in this hilarious Gorilla Tag adventure!",
                featured=True
            ),
            Video(
                title="How to NOT Play Gorilla Tag",
                youtube_id="dQw4w9WgXcQ",
                description="MoxxieVR shows all the wrong ways to play Gorilla Tag.",
                featured=True
            ),
            Video(
                title="Banana Hunt Challenge",
                youtube_id="dQw4w9WgXcQ",
                description="Can MoxxieVR find all the hidden bananas? Probably not.",
                featured=True
            ),
        ]
        db.session.add_all(videos)
        db.session.commit()


@app.route('/')
def index():
    # Record site visit
    new_visit = SiteVisit(
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string,
        page_visited='home'
    )
    db.session.add(new_visit)
    db.session.commit()
    
    return send_from_directory('.', 'index.html')

@app.route('/api/videos')
def get_videos():
    videos = Video.query.filter_by(featured=True).all()
    result = []
    for video in videos:
        result.append({
            'id': video.id,
            'title': video.title,
            'youtube_id': video.youtube_id,
            'description': video.description,
            'views': video.views,
            'likes': video.likes
        })
    return jsonify(result)

@app.route('/api/memes/templates')
def get_meme_templates():
    templates = MemeTemplate.query.all()
    result = []
    for template in templates:
        result.append({
            'id': template.id,
            'name': template.name,
            'emoji': template.emoji
        })
    return jsonify(result)

@app.route('/api/memes/create', methods=['POST'])
def create_meme():
    data = request.get_json()
    
    if not data or 'template_id' not in data:
        return jsonify({'error': 'Missing template_id'}), 400
    
    new_meme = CreatedMeme(
        top_text=data.get('top_text', ''),
        bottom_text=data.get('bottom_text', ''),
        template_id=data['template_id']
    )
    
    db.session.add(new_meme)
    db.session.commit()
    
    return jsonify({'success': True, 'meme_id': new_meme.id})

@app.route('/api/game/score', methods=['POST'])
def save_game_score():
    data = request.get_json()
    
    if not data or 'score' not in data or 'player_name' not in data:
        return jsonify({'error': 'Missing score or player_name'}), 400
    
    new_score = BananaScore(
        player_name=data['player_name'],
        score=data['score']
    )
    
    db.session.add(new_score)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/game/highscores')
def get_highscores():
    scores = BananaScore.query.order_by(BananaScore.score.desc()).limit(10).all()
    result = []
    for score in scores:
        result.append({
            'player_name': score.player_name,
            'score': score.score,
            'date': score.created_at.strftime('%Y-%m-%d')
        })
    return jsonify(result)

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    
    if not data or 'email' not in data:
        return jsonify({'error': 'Missing email'}), 400
    
    # Check if email already exists
    existing = Subscriber.query.filter_by(email=data['email']).first()
    if existing:
        return jsonify({'error': 'Email already subscribed'}), 400
    
    new_subscriber = Subscriber(
        email=data['email'],
        name=data.get('name', None)
    )
    
    db.session.add(new_subscriber)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({'error': 'Missing message'}), 400
    
    new_feedback = Feedback(
        name=data.get('name', None),
        email=data.get('email', None),
        message=data['message']
    )
    
    db.session.add(new_feedback)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/easter-egg/<egg_name>', methods=['POST'])
def found_easter_egg(egg_name):
    # Find or create easter egg record
    egg = EasterEggFound.query.filter_by(egg_name=egg_name).first()
    
    if egg:
        egg.found_count += 1
        egg.last_found_at = datetime.utcnow()
    else:
        egg = EasterEggFound(
            egg_name=egg_name,
            found_count=1
        )
        db.session.add(egg)
    
    db.session.commit()
    
    return jsonify({'success': True, 'found_count': egg.found_count})

# Special route for handling 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)