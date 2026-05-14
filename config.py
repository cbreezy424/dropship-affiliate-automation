import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dropship.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Folders
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    VIDEO_OUTPUT_FOLDER = os.getenv('VIDEO_OUTPUT_FOLDER', 'videos')
    TEMP_FOLDER = os.getenv('TEMP_FOLDER', 'temp')
    
    # Create folders if they don't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(VIDEO_OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    
    # API Keys
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    AMAZON_AFFILIATE_ID = os.getenv('AMAZON_AFFILIATE_ID', '')
    AMAZON_REGION = os.getenv('AMAZON_REGION', 'com')
    
    # Video Settings
    VIDEO_FRAME_RATE = int(os.getenv('VIDEO_FRAME_RATE', 30))
    VIDEO_QUALITY = os.getenv('VIDEO_QUALITY', '720p')
    VIDEO_DURATION = int(os.getenv('VIDEO_DURATION', 30))
    VOICE_LANGUAGE = os.getenv('VOICE_LANGUAGE', 'en')
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
