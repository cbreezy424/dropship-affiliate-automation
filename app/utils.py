import os
import uuid
from slugify import slugify
from urllib.parse import urljoin

def generate_slug(text):
    """Generate URL-friendly slug from text"""
    return slugify(text)

def generate_unique_filename(filename):
    """Generate unique filename to avoid conflicts"""
    name, ext = os.path.splitext(filename)
    unique_name = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
    return unique_name

def ensure_directory(path):
    """Ensure directory exists"""
    os.makedirs(path, exist_ok=True)

def get_file_size(filepath):
    """Get file size in MB"""
    if os.path.exists(filepath):
        size_bytes = os.path.getsize(filepath)
        return size_bytes / (1024 * 1024)
    return 0

def format_video_duration(seconds):
    """Format seconds to MM:SS"""
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"
