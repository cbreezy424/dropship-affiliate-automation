from app import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500))
    amazon_asin = db.Column(db.String(50))
    aliexpress_url = db.Column(db.String(500))
    affiliate_link = db.Column(db.String(500))
    category = db.Column(db.String(100))
    slug = db.Column(db.String(255), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    scripts = db.relationship('Script', backref='product', lazy=True, cascade='all, delete-orphan')
    videos = db.relationship('Video', backref='product', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url,
            'amazon_asin': self.amazon_asin,
            'affiliate_link': self.affiliate_link,
            'category': self.category,
            'created_at': self.created_at.isoformat(),
        }

class Script(db.Model):
    __tablename__ = 'scripts'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tone = db.Column(db.String(50), default='professional')  # professional, casual, funny
    language = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'content': self.content,
            'tone': self.tone,
            'language': self.language,
            'created_at': self.created_at.isoformat(),
        }

class Video(db.Model):
    __tablename__ = 'videos'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    script_id = db.Column(db.Integer, db.ForeignKey('scripts.id'))
    file_path = db.Column(db.String(500), nullable=False)
    duration = db.Column(db.Integer)  # in seconds
    format = db.Column(db.String(20), default='mp4')  # mp4, avi, mov
    platform = db.Column(db.String(50))  # tiktok, instagram, youtube
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'file_path': self.file_path,
            'duration': self.duration,
            'format': self.format,
            'platform': self.platform,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
        }

class SocialPost(db.Model):
    __tablename__ = 'social_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'))
    platform = db.Column(db.String(50))  # tiktok, instagram, youtube
    post_url = db.Column(db.String(500))
    scheduled_at = db.Column(db.DateTime)
    posted_at = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='draft')  # draft, scheduled, posted
    caption = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'video_id': self.video_id,
            'platform': self.platform,
            'status': self.status,
            'caption': self.caption,
            'created_at': self.created_at.isoformat(),
        }
