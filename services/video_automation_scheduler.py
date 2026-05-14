import schedule
import time
from datetime import datetime
import threading
import os
from app import create_app, db
from app.models import Product, Script, Video, SocialPost
from services.product_scraper import ProductScraper
from services.script_generator import ScriptGenerator
from services.video_creator import VideoCreator
from services.social_media_automation import SocialMediaAutomation

class VideoAutomationScheduler:
    """Service for scheduling automated video generation and posting"""
    
    def __init__(self):
        self.app = create_app()
        self.scraper = ProductScraper()
        self.script_gen = ScriptGenerator()
        self.video_creator = VideoCreator()
        self.social_media = SocialMediaAutomation()
        self.is_running = False
        self.scheduler_thread = None
    
    def generate_video_batch(self, num_videos=5, categories=None):
        """
        Generate a batch of videos
        
        Args:
            num_videos: Number of videos to generate
            categories: List of categories (health, wealth, wellness)
        
        Returns:
            List of generated video paths
        """
        
        if categories is None:
            categories = ['health', 'wealth', 'wellness']
        
        print(f"\n🎬 Generating {num_videos} videos...")
        generated_videos = []
        
        with self.app.app_context():
            try:
                # Step 1: Scrape products
                print("\n🔍 Scraping trending products...")
                scraped_products = self.scraper.scrape_all_categories(limit=num_videos * 3)
                
                if not scraped_products:
                    print("⚠️  No products scraped, using sample products")
                    scraped_products = self.scraper.get_sample_products()
                
                # Filter to requested number and categories
                filtered_products = [
                    p for p in scraped_products 
                    if p.get('category') in categories
                ][:num_videos]
                
                print(f"✓ Found {len(filtered_products)} products")
                
                # Step 2: Add products to database if not exist
                for product_data in filtered_products:
                    existing = Product.query.filter_by(name=product_data.get('name')).first()
                    
                    if not existing:
                        product = Product(
                            name=product_data.get('name'),
                            description=product_data.get('description', ''),
                            price=product_data.get('price', 0),
                            image_url=product_data.get('image_url', 'https://via.placeholder.com/500x500'),
                            amazon_asin=product_data.get('amazon_asin'),
                            aliexpress_url=product_data.get('aliexpress_url'),
                            category=product_data.get('category'),
                            slug=product_data.get('name', '').lower().replace(' ', '-')
                        )
                        db.session.add(product)
                    else:
                        product = existing
                
                db.session.commit()
                print(f"✓ Added products to database")
                
                # Step 3: Generate scripts
                print("\n📝 Generating scripts...")
                for i, product_data in enumerate(filtered_products, 1):
                    product = Product.query.filter_by(name=product_data.get('name')).first()
                    
                    if product and not Script.query.filter_by(product_id=product.id).first():
                        script_content = self.script_gen.generate_script(
                            product_name=product.name,
                            product_description=product.description,
                            price=product.price,
                            tone='casual'
                        )
                        
                        script = Script(
                            product_id=product.id,
                            content=script_content,
                            tone='casual'
                        )
                        db.session.add(script)
                        print(f"  {i}. Script generated for {product.name}")
                
                db.session.commit()
                print(f"✓ Scripts generated")
                
                # Step 4: Create videos
                print("\n🎥 Creating videos...")
                for i, product_data in enumerate(filtered_products, 1):
                    try:
                        product = Product.query.filter_by(name=product_data.get('name')).first()
                        script = Script.query.filter_by(product_id=product.id).first()
                        
                        if product and script:
                            # Create videos for each platform
                            platforms = ['tiktok', 'instagram', 'facebook', 'youtube']
                            
                            for platform in platforms:
                                try:
                                    video_path = self.video_creator.create_video(
                                        product_image_url=product.image_url or 'https://via.placeholder.com/500x500',
                                        script_text=script.content,
                                        product_name=product.name,
                                        platform=platform,
                                        duration=30
                                    )
                                    
                                    video = Video(
                                        product_id=product.id,
                                        script_id=script.id,
                                        file_path=video_path,
                                        format='mp4',
                                        platform=platform,
                                        status='completed'
                                    )
                                    db.session.add(video)
                                    generated_videos.append(video_path)
                                    print(f"  {i}. Video created for {product.name} ({platform})")
                                
                                except Exception as e:
                                    print(f"  ⚠️  Error creating {platform} video: {str(e)}")
                                    continue
                    
                    except Exception as e:
                        print(f"  ⚠️  Error processing product: {str(e)}")
                        continue
                
                db.session.commit()
                print(f"✓ Videos created: {len(generated_videos)}")
                
                # Step 5: Create social posts
                print("\n📱 Creating social posts...")
                videos = Video.query.filter_by(status='completed').all()
                
                for video in videos[-num_videos*4:]:
                    product = Product.query.get(video.product_id)
                    
                    caption = self.social_media.generate_platform_captions(
                        product.name,
                        product.description,
                        video.platform
                    )
                    
                    post = SocialPost(
                        video_id=video.id,
                        platform=video.platform,
                        caption=caption,
                        status='draft'
                    )
                    db.session.add(post)
                
                db.session.commit()
                print(f"✓ Social posts created")
                
                print(f"\n✅ Batch complete! Generated {len(generated_videos)} videos")
                return generated_videos
            
            except Exception as e:
                print(f"\n❌ Error in batch generation: {str(e)}")
                db.session.rollback()
                return []
    
    def daily_job(self):
        """
        Daily automation job
        """
        print(f"\n{'='*60}")
        print(f"🤖 DAILY AUTOMATION JOB - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        self.generate_video_batch(num_videos=5)
    
    def start_scheduler(self, schedule_time='00:00', interval='daily'):
        """
        Start the scheduler
        
        Args:
            schedule_time: Time to run (HH:MM format)
            interval: 'daily', 'hourly', or 'minute'
        """
        
        if self.is_running:
            print("⚠️  Scheduler already running")
            return
        
        self.is_running = True
        
        # Schedule jobs
        if interval == 'daily':
            schedule.every().day.at(schedule_time).do(self.daily_job)
            print(f"✓ Scheduled daily at {schedule_time} UTC")
        elif interval == 'hourly':
            schedule.every().hour.do(self.daily_job)
            print(f"✓ Scheduled every hour")
        elif interval == 'minute':
            schedule.every().minute.do(self.daily_job)
            print(f"✓ Scheduled every minute")
        
        # Run scheduler in separate thread
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        print("✓ Scheduler thread started")
    
    def _run_scheduler(self):
        """
        Run scheduler loop
        """
        print("🔄 Scheduler running...")
        
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                print(f"Scheduler error: {str(e)}")
                time.sleep(60)
    
    def stop_scheduler(self):
        """
        Stop the scheduler
        """
        self.is_running = False
        print("✓ Scheduler stopped")
    
    def get_stats(self):
        """
        Get automation statistics
        
        Returns:
            Dictionary with stats
        """
        
        with self.app.app_context():
            stats = {
                'total_products': Product.query.count(),
                'total_scripts': Script.query.count(),
                'total_videos': Video.query.count(),
                'total_social_posts': SocialPost.query.count(),
                'videos_by_platform': {},
                'videos_by_status': {},
                'latest_videos': []
            }
            
            # Videos by platform
            for platform in ['tiktok', 'instagram', 'facebook', 'youtube']:
                count = Video.query.filter_by(platform=platform).count()
                stats['videos_by_platform'][platform] = count
            
            # Videos by status
            for status in ['pending', 'processing', 'completed', 'failed']:
                count = Video.query.filter_by(status=status).count()
                stats['videos_by_status'][status] = count
            
            # Latest videos
            latest = Video.query.order_by(Video.created_at.desc()).limit(5).all()
            stats['latest_videos'] = [{
                'id': v.id,
                'product': Product.query.get(v.product_id).name,
                'platform': v.platform,
                'status': v.status,
                'created_at': v.created_at.isoformat()
            } for v in latest]
            
            return stats
