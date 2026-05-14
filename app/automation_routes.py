from flask import Blueprint, request, jsonify
from services.video_automation_scheduler import VideoAutomationScheduler
from services.product_scraper import ProductScraper
from services.script_generator import ScriptGenerator
from services.video_creator import VideoCreator
from services.social_media_automation import SocialMediaAutomation
from app.models import Product, Script, Video, SocialPost
from app import db
from threading import Thread

automation_bp = Blueprint('automation', __name__)

scheduler = VideoAutomationScheduler()
scraper = ProductScraper()
script_gen = ScriptGenerator()
video_creator = VideoCreator()
social_media = SocialMediaAutomation()

# Global scheduler instance
_scheduler_instance = None

@automation_bp.route('/scrape/products', methods=['POST'])
def scrape_products():
    """
    Scrape trending products
    
    POST /api/automation/scrape/products
    body: {
        "category": "health",
        "limit": 50,
        "min_rating": 3.5
    }
    """
    data = request.json or {}
    
    category = data.get('category', 'health')
    limit = data.get('limit', 50)
    
    try:
        # Scrape products
        if category == 'all':
            products = scraper.scrape_all_categories(limit=limit)
        else:
            products = []
            products.extend(scraper.scrape_aliexpress_products(category, limit // 3))
            products.extend(scraper.scrape_amazon_products(category, limit // 3))
            products.extend(scraper.scrape_ebay_products(category, limit // 3))
            
            # Filter quality
            products = scraper.filter_quality_products(products)
        
        if not products:
            products = scraper.get_sample_products()
        
        return jsonify({
            'success': True,
            'count': len(products),
            'products': products[:limit]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@automation_bp.route('/trending/products', methods=['GET'])
def get_trending_products():
    """
    Get trending products
    
    GET /api/automation/trending/products?limit=50
    """
    limit = request.args.get('limit', 50, type=int)
    
    try:
        products = scraper.scrape_all_categories(limit=limit)
        
        if not products:
            products = scraper.get_sample_products()
        
        return jsonify({
            'success': True,
            'count': len(products),
            'products': products
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@automation_bp.route('/generate/videos', methods=['POST'])
def generate_videos():
    """
    Generate videos in background
    
    POST /api/automation/generate/videos
    body: {"num_videos": 5}
    """
    data = request.json or {}
    num_videos = data.get('num_videos', 5)
    
    def background_generation():
        try:
            scheduler.generate_video_batch(num_videos=num_videos)
        except Exception as e:
            print(f"Background generation error: {str(e)}")
    
    # Run in background thread
    thread = Thread(target=background_generation, daemon=True)
    thread.start()
    
    return jsonify({
        'success': True,
        'message': f'Generating {num_videos} videos in background...',
        'num_videos': num_videos
    })

@automation_bp.route('/product/convert', methods=['POST'])
def convert_product_to_video():
    """
    Convert single product to video
    
    POST /api/automation/product/convert
    body: {
        "name": "Yoga Mat",
        "description": "Premium yoga mat",
        "price": 29.99,
        "image_url": "https://...",
        "category": "wellness"
    }
    """
    data = request.json or {}
    
    try:
        # Create product
        product = Product(
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            image_url=data.get('image_url', 'https://via.placeholder.com/500x500'),
            category=data.get('category'),
            slug=data.get('name', '').lower().replace(' ', '-')
        )
        db.session.add(product)
        db.session.commit()
        
        # Generate script
        script_content = script_gen.generate_script(
            product_name=product.name,
            product_description=product.description,
            price=product.price
        )
        
        script = Script(
            product_id=product.id,
            content=script_content
        )
        db.session.add(script)
        db.session.commit()
        
        # Create video
        video_path = video_creator.create_video(
            product_image_url=product.image_url,
            script_text=script_content,
            product_name=product.name,
            platform='tiktok'
        )
        
        video = Video(
            product_id=product.id,
            script_id=script.id,
            file_path=video_path,
            platform='tiktok',
            status='completed'
        )
        db.session.add(video)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'product': product.to_dict(),
            'video': video.to_dict(),
            'script': script.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@automation_bp.route('/schedule/daily', methods=['POST'])
def schedule_daily():
    """
    Start daily scheduler
    
    POST /api/automation/schedule/daily
    body: {"videos_per_day": 5}
    """
    global _scheduler_instance
    
    data = request.json or {}
    videos_per_day = data.get('videos_per_day', 5)
    
    try:
        if _scheduler_instance is None:
            _scheduler_instance = VideoAutomationScheduler()
        
        _scheduler_instance.start_scheduler(schedule_time='00:00', interval='daily')
        
        return jsonify({
            'success': True,
            'message': f'Daily scheduler started ({videos_per_day} videos/day)',
            'schedule': 'Daily at 00:00 UTC'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@automation_bp.route('/schedule/stop', methods=['POST'])
def stop_scheduler():
    """
    Stop the scheduler
    
    POST /api/automation/schedule/stop
    """
    global _scheduler_instance
    
    try:
        if _scheduler_instance:
            _scheduler_instance.stop_scheduler()
        
        return jsonify({
            'success': True,
            'message': 'Scheduler stopped'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@automation_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Get automation statistics
    
    GET /api/automation/stats
    """
    try:
        stats = scheduler.get_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@automation_bp.route('/videos/list', methods=['GET'])
def list_videos():
    """
    List all generated videos
    
    GET /api/automation/videos/list?page=1&per_page=20
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    try:
        videos_paginated = Video.query.paginate(page=page, per_page=per_page)
        
        videos = []
        for video in videos_paginated.items:
            product = Product.query.get(video.product_id)
            post = SocialPost.query.filter_by(video_id=video.id).first()
            
            videos.append({
                'video': video.to_dict(),
                'product': product.to_dict() if product else None,
                'post': post.to_dict() if post else None
            })
        
        return jsonify({
            'success': True,
            'videos': videos,
            'total': videos_paginated.total,
            'pages': videos_paginated.pages,
            'current_page': page
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
