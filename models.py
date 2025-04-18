from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Subscriber {self.email}>'

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    youtube_id = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    featured = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Video {self.title}>'

class MemeTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    emoji = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with CreatedMeme
    memes = db.relationship('CreatedMeme', backref='template', lazy=True)
    
    def __repr__(self):
        return f'<MemeTemplate {self.name}>'

class CreatedMeme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    top_text = db.Column(db.String(200), nullable=True)
    bottom_text = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key relationship with MemeTemplate
    template_id = db.Column(db.Integer, db.ForeignKey('meme_template.id'), nullable=False)
    
    def __repr__(self):
        return f'<CreatedMeme {self.id}>'

class BananaScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BananaScore {self.player_name}: {self.score}>'

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Feedback {self.id}>'

class SiteVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    page_visited = db.Column(db.String(100), nullable=False)
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SiteVisit {self.page_visited}>'

class EasterEggFound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    egg_name = db.Column(db.String(100), nullable=False)
    found_count = db.Column(db.Integer, default=0)
    last_found_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EasterEggFound {self.egg_name}: {self.found_count}>'