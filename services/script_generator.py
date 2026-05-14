import os
from groq import Groq

class ScriptGenerator:
    """Service for generating product scripts using Groq API"""
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.model = "mixtral-8x7b-32768"
    
    def generate_script(self, product_name, product_description, price, tone='professional', duration_seconds=30):
        """
        Generate engaging product script using Groq
        
        Args:
            product_name: Name of the product
            product_description: Product description/features
            price: Product price
            tone: Script tone (professional, casual, funny)
            duration_seconds: Target video duration (30, 60)
        
        Returns:
            Script text optimized for video
        """
        
        prompt = self._build_prompt(product_name, product_description, price, tone, duration_seconds)
        
        try:
            message = self.client.messages.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1024,
                temperature=0.7
            )
            
            return message.content[0].text
        except Exception as e:
            print(f"Error generating script: {str(e)}")
            return self._generate_fallback_script(product_name, product_description, price)
    
    def _build_prompt(self, product_name, product_description, price, tone, duration_seconds):
        """Build prompt for script generation"""
        
        tone_description = {
            'professional': 'professional and authoritative',
            'casual': 'casual and friendly',
            'funny': 'humorous and entertaining'
        }.get(tone, 'professional')
        
        word_count = (duration_seconds // 10) * 25  # ~2.5 words per second
        
        prompt = f"""
        Create a compelling {duration_seconds}-second social media video script for this product:
        
        Product Name: {product_name}
        Description: {product_description}
        Price: ${price}
        Tone: {tone_description}
        Target Word Count: ~{word_count} words
        
        Requirements:
        - Start with a hook that grabs attention in first 3 seconds
        - Highlight key benefits and features
        - Include a call-to-action at the end
        - Use conversational, engaging language
        - Optimize for TikTok/Instagram Reels/YouTube Shorts
        - Include [PAUSE] markers for visual transitions
        
        Format as continuous script (not bullet points).
        """
        
        return prompt
    
    def _generate_fallback_script(self, product_name, product_description, price):
        """Generate fallback script if API fails"""
        return f"""
Hey! Check out this amazing {product_name}! 

{product_description}

For just ${price}, you can't beat this deal. 

Click the link in bio to grab yours today before they're gone!
        """
    
    def generate_multiple_scripts(self, product_name, product_description, price, tones=None, count=3):
        """Generate multiple script variations"""
        if tones is None:
            tones = ['professional', 'casual', 'funny']
        
        scripts = []
        for tone in tones[:count]:
            script = self.generate_script(product_name, product_description, price, tone)
            scripts.append({
                'tone': tone,
                'content': script
            })
        
        return scripts
