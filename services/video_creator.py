import os
import subprocess
from urllib.request import urlretrieve
from app.utils import ensure_directory, generate_unique_filename
from services.tts_service import TTSService

class VideoCreator:
    """Service for creating videos with images and voiceovers"""
    
    def __init__(self):
        self.output_folder = os.getenv('VIDEO_OUTPUT_FOLDER', 'videos')
        self.temp_folder = os.getenv('TEMP_FOLDER', 'temp')
        self.tts_service = TTSService()
        ensure_directory(self.output_folder)
        ensure_directory(self.temp_folder)
    
    def create_video(self, product_image_url, script_text, product_name, platform='tiktok', duration=30):
        """
        Create video with product image and voiceover
        
        Args:
            product_image_url: URL of product image
            script_text: Script for voiceover
            product_name: Product name
            platform: Target platform (tiktok, instagram, youtube)
            duration: Video duration in seconds
        
        Returns:
            Path to created video file
        """
        
        try:
            # Step 1: Download product image
            image_path = self._download_image(product_image_url)
            
            # Step 2: Generate voiceover
            audio_path = self.tts_service.text_to_speech(script_text)
            
            # Step 3: Create video with FFmpeg
            video_path = self._create_video_with_ffmpeg(image_path, audio_path, product_name, platform, duration)
            
            # Step 4: Cleanup temp files
            self._cleanup_temp_files(image_path, audio_path)
            
            return video_path
        
        except Exception as e:
            print(f"Error creating video: {str(e)}")
            raise
    
    def _download_image(self, image_url):
        """
        Download image from URL
        
        Returns:
            Path to downloaded image
        """
        try:
            filename = generate_unique_filename('product.jpg')
            filepath = os.path.join(self.temp_folder, filename)
            urlretrieve(image_url, filepath)
            return filepath
        except Exception as e:
            print(f"Error downloading image: {str(e)}")
            raise
    
    def _create_video_with_ffmpeg(self, image_path, audio_path, product_name, platform, duration):
        """
        Create video using FFmpeg
        
        Args:
            image_path: Path to product image
            audio_path: Path to voiceover audio
            product_name: Product name
            platform: Target platform
            duration: Video duration
        
        Returns:
            Path to created video
        """
        
        try:
            # Define video dimensions based on platform
            dimensions = {
                'tiktok': '1080x1920',
                'instagram': '1080x1920',
                'youtube': '1280x720'
            }
            
            video_size = dimensions.get(platform, '1080x1920')
            
            # Generate output filename
            output_filename = generate_unique_filename(f'{product_name}.mp4')
            output_path = os.path.join(self.output_folder, output_filename)
            
            # FFmpeg command
            cmd = [
                'ffmpeg',
                '-loop', '1',
                '-i', image_path,
                '-i', audio_path,
                '-c:v', 'libx264',
                '-tune', 'stillimage',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-pix_fmt', 'yuv420p',
                '-s', video_size,
                '-shortest',
                '-y',
                output_path
            ]
            
            # Run FFmpeg
            subprocess.run(cmd, check=True, capture_output=True)
            
            print(f"Video created: {output_path}")
            return output_path
        
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e.stderr.decode()}")
            raise
        except Exception as e:
            print(f"Error creating video with FFmpeg: {str(e)}")
            raise
    
    def _cleanup_temp_files(self, *file_paths):
        """Clean up temporary files"""
        for filepath in file_paths:
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as e:
                print(f"Error cleaning up file {filepath}: {str(e)}")
