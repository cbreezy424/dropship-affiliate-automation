from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import Product, Script, Video, SocialPost
from services.product_service import ProductService
from services.script_generator import ScriptGenerator
from services.video_creator import VideoCreator
from services.affiliate_manager import AffiliateManager
import os

main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

product_service = ProductService()
script_gen = ScriptGenerator()
video_creator = VideoCreator()
affiliate_mgr = AffiliateManager()

# Main Routes
@main_bp.route('/')
def index():
    stats = {
        'total_products': Product.query.count(),
        'total_scripts': Script.query.count(),
        'total_videos': Video.query.count(),
        'total_posts': SocialPost.query.count(),
    }
    return render_template('index.html', stats=stats)

@main_bp.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    products_list = Product.query.paginate(page=page, per_page=20)
    return render_template('products.html', products=products_list)

@main_bp.route('/videos')
def videos():
    page = request.args.get('page', 1, type=int)
    videos_list = Video.query.paginate(page=page, per_page=20)
    return render_template('videos.html', videos=videos_list)

@main_bp.route('/settings')
def settings():
    return render_template('settings.html')

# API Routes - Products
@api_bp.route('/products', methods=['GET'])
def get_products():
    products_list = Product.query.all()
    return jsonify([p.to_dict() for p in products_list])

@api_bp.route('/products', methods=['POST'])
def create_product():
    data = request.json
    
    # Generate affiliate link
    affiliate_link = affiliate_mgr.generate_amazon_link(data.get('amazon_asin'))
    
    product = Product(
        name=data.get('name'),
        description=data.get('description'),
        price=data.get('price'),
        image_url=data.get('image_url'),
        amazon_asin=data.get('amazon_asin'),
        aliexpress_url=data.get('aliexpress_url'),
        affiliate_link=affiliate_link,
        category=data.get('category'),
        slug=data.get('name', '').lower().replace(' ', '-')
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify(product.to_dict()), 201

@api_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@api_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json
    
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.image_url = data.get('image_url', product.image_url)
    product.category = data.get('category', product.category)
    
    db.session.commit()
    return jsonify(product.to_dict())

@api_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return '', 204

# API Routes - Scripts
@api_bp.route('/products/<int:product_id>/scripts', methods=['POST'])
def generate_script(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json
    
    tone = data.get('tone', 'professional')
    
    script_content = script_gen.generate_script(
        product_name=product.name,
        product_description=product.description,
        price=product.price,
        tone=tone
    )
    
    script = Script(
        product_id=product_id,
        content=script_content,
        tone=tone
    )
    
    db.session.add(script)
    db.session.commit()
    
    return jsonify(script.to_dict()), 201

@api_bp.route('/scripts', methods=['GET'])
def get_scripts():
    scripts_list = Script.query.all()
    return jsonify([s.to_dict() for s in scripts_list])

# API Routes - Videos
@api_bp.route('/videos/create', methods=['POST'])
def create_video():
    data = request.json
    product_id = data.get('product_id')
    script_id = data.get('script_id')
    platform = data.get('platform', 'tiktok')  # tiktok, instagram, youtube
    
    product = Product.query.get_or_404(product_id)
    script = Script.query.get_or_404(script_id) if script_id else None
    
    try:
        video_path = video_creator.create_video(
            product_image_url=product.image_url,
            script_text=script.content if script else product.description,
            product_name=product.name,
            platform=platform
        )
        
        video = Video(
            product_id=product_id,
            script_id=script_id,
            file_path=video_path,
            format='mp4',
            platform=platform,
            status='completed'
        )
        
        db.session.add(video)
        db.session.commit()
        
        return jsonify(video.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/videos', methods=['GET'])
def get_videos():
    videos_list = Video.query.all()
    return jsonify([v.to_dict() for v in videos_list])

@api_bp.route('/videos/<int:video_id>/download', methods=['GET'])
def download_video(video_id):
    video = Video.query.get_or_404(video_id)
    return jsonify({
        'video_id': video.id,
        'file_path': video.file_path,
        'download_url': f'/videos/{os.path.basename(video.file_path)}'
    })

# API Routes - Social Posts
@api_bp.route('/social-posts', methods=['POST'])
def create_social_post():
    data = request.json
    
    post = SocialPost(
        video_id=data.get('video_id'),
        platform=data.get('platform'),
        caption=data.get('caption'),
        status='draft'
    )
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify(post.to_dict()), 201

@api_bp.route('/social-posts', methods=['GET'])
def get_social_posts():
    posts = SocialPost.query.all()
    return jsonify([p.to_dict() for p in posts])

# Health check
@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})
