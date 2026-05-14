import requests
import json
from datetime import datetime, timedelta
import os

class SocialMediaAutomation:
    """Service for posting videos to social media platforms"""
    
    def __init__(self):
        self.tiktok_token = os.getenv('TIKTOK_ACCESS_TOKEN')
        self.instagram_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        self.facebook_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.youtube_key = os.getenv('YOUTUBE_API_KEY')
    
    def generate_platform_captions(self, product_name, product_description, platform):
        """
        Generate platform-specific captions
        
        Args:
            product_name: Product name
            product_description: Product description
            platform: tiktok, instagram, facebook, youtube
        
        Returns:
            Caption text optimized for platform
        """
        
        captions = {
            'tiktok': self._tiktok_caption(product_name, product_description),
            'instagram': self._instagram_caption(product_name, product_description),
            'facebook': self._facebook_caption(product_name, product_description),
            'youtube': self._youtube_caption(product_name, product_description),
        }
        
        return captions.get(platform, captions['tiktok'])
    
    def _tiktok_caption(self, product_name, description):
        """Generate TikTok caption with hashtags"""
        return f"""✨ Check out this amazing {product_name}! 

{description[:100]}... 

Link in bio! 🔗

#FYP #ForYou #ProductReview #Wellness #Shopping #TikTokShop
        """.strip()
    
    def _instagram_caption(self, product_name, description):
        """Generate Instagram caption with hashtags"""
        return f"""🆆 {product_name}

{description[:80]}...

✨ Link in bio ✨

#wellness #product #shopping #instagram #instagood #reels #foryoupage
        """.strip()
    
    def _facebook_caption(self, product_name, description):
        """Generate Facebook caption"""
        return f"""👏 Discover: {product_name}

{description}

Click below to learn more! 👇
        """.strip()
    
    def _youtube_caption(self, product_name, description):
        """Generate YouTube caption with links"""
        return f"""{product_name} Review & Unboxing

{description}

BUY NOW: [Link in description]

📱 Follow us:
- Instagram: [link]
- TikTok: [link]
- Facebook: [link]

Thanks for watching! Don't forget to like and subscribe!
        """.strip()
    
    def post_to_tiktok(self, video_path, caption, hashtags=None):
        """
        Post video to TikTok
        
        Args:
            video_path: Path to video file
            caption: Video caption
            hashtags: List of hashtags
        
        Returns:
            Success/failure status
        """
        
        if not self.tiktok_token:
            print("⚠️  TikTok token not configured. Set TIKTOK_ACCESS_TOKEN in .env")
            return {'success': False, 'message': 'Token not configured'}
        
        try:
            url = "https://open.tiktokapis.com/v1/video/upload/"
            
            headers = {
                'Authorization': f'Bearer {self.tiktok_token}'
            }
            
            with open(video_path, 'rb') as f:
                files = {'video': f}
                data = {
                    'description': caption,
                    'privacy_level': 'PUBLIC'
                }
                
                response = requests.post(url, headers=headers, files=files, data=data)
            
            if response.status_code == 200:
                return {'success': True, 'platform': 'tiktok', 'post_id': response.json().get('data', {}).get('video_id')}
            else:
                return {'success': False, 'error': response.text}
        
        except Exception as e:
            print(f"TikTok posting error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def post_to_instagram(self, video_path, caption):
        """
        Post Reel to Instagram
        
        Args:
            video_path: Path to video file
            caption: Video caption
        
        Returns:
            Success/failure status
        """
        
        if not self.instagram_token:
            print("⚠️  Instagram token not configured. Set INSTAGRAM_ACCESS_TOKEN in .env")
            return {'success': False, 'message': 'Token not configured'}
        
        try:
            url = "https://graph.instagram.com/v18.0/me/media"
            
            params = {
                'access_token': self.instagram_token,
                'media_type': 'REELS',
                'video_url': video_path,  # Should be publicly accessible URL
                'caption': caption
            }
            
            response = requests.post(url, params=params)
            
            if response.status_code == 200:
                return {'success': True, 'platform': 'instagram', 'post_id': response.json().get('id')}
            else:
                return {'success': False, 'error': response.text}
        
        except Exception as e:
            print(f"Instagram posting error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def post_to_facebook(self, video_path, caption):
        """
        Post video to Facebook
        
        Args:
            video_path: Path to video file
            caption: Video caption
        
        Returns:
            Success/failure status
        """
        
        if not self.facebook_token:
            print("⚠️  Facebook token not configured. Set FACEBOOK_ACCESS_TOKEN in .env")
            return {'success': False, 'message': 'Token not configured'}
        
        try:
            url = "https://graph.facebook.com/v18.0/me/videos"
            
            params = {'access_token': self.facebook_token}
            
            with open(video_path, 'rb') as f:
                files = {'source': f}
                data = {'description': caption}
                
                response = requests.post(url, params=params, files=files, data=data)
            
            if response.status_code == 200:
                return {'success': True, 'platform': 'facebook', 'post_id': response.json().get('id')}
            else:
                return {'success': False, 'error': response.text}
        
        except Exception as e:
            print(f"Facebook posting error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def upload_to_youtube(self, video_path, title, description, tags=None):
        """
        Upload video to YouTube
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
        
        Returns:
            Success/failure status
        """
        
        if not self.youtube_key:
            print("⚠️  YouTube API key not configured. Set YOUTUBE_API_KEY in .env")
            return {'success': False, 'message': 'API key not configured'}
        
        try:
            # Note: YouTube requires OAuth2 for uploads, not simple API key
            # This is a simplified version - real implementation needs OAuth flow
            
            print(f"📤 YouTube upload preparation for: {title}")
            print(f"📁 Video: {video_path}")
            print(f"📝 Description: {description[:50]}...")
            
            return {
                'success': True,
                'platform': 'youtube',
                'message': 'Video ready for upload (manual upload required)',
                'video_file': video_path
            }
        
        except Exception as e:
            print(f"YouTube upload error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def schedule_post(self, platform, video_path, caption, schedule_time=None):
        """
        Schedule post for later
        
        Args:
            platform: tiktok, instagram, facebook, youtube
            video_path: Path to video
            caption: Video caption
            schedule_time: datetime for scheduling
        
        Returns:
            Scheduled post info
        """
        
        if schedule_time is None:
            schedule_time = datetime.utcnow() + timedelta(hours=1)
        
        return {
            'platform': platform,
            'video_path': video_path,
            'caption': caption,
            'scheduled_time': schedule_time.isoformat(),
            'status': 'scheduled'
        }
    
    def post_to_all_platforms(self, video_path, product_name, product_description):
        """
        Post video to all platforms at once
        
        Args:
            video_path: Path to video
            product_name: Product name
            product_description: Product description
        
        Returns:
            List of posting results
        """
        
        results = []
        platforms = ['tiktok', 'instagram', 'facebook', 'youtube']
        
        for platform in platforms:
            caption = self.generate_platform_captions(product_name, product_description, platform)
            
            if platform == 'tiktok':
                result = self.post_to_tiktok(video_path, caption)
            elif platform == 'instagram':
                result = self.post_to_instagram(video_path, caption)
            elif platform == 'facebook':
                result = self.post_to_facebook(video_path, caption)
            elif platform == 'youtube':
                result = self.upload_to_youtube(video_path, product_name, caption)
            
            results.append(result)
        
        return results
