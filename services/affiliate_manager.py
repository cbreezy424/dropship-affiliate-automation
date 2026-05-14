import os
from urllib.parse import urlencode

class AffiliateManager:
    """Service for managing affiliate links"""
    
    def __init__(self):
        self.amazon_affiliate_id = os.getenv('AMAZON_AFFILIATE_ID', '')
        self.amazon_region = os.getenv('AMAZON_REGION', 'com')
    
    def generate_amazon_link(self, asin, tag=None):
        """
        Generate Amazon affiliate link
        
        Args:
            asin: Amazon Standard Identification Number
            tag: Affiliate tag (defaults to configured tag)
        
        Returns:
            Amazon affiliate URL
        """
        
        if not asin:
            return None
        
        tag = tag or self.amazon_affiliate_id
        region = self.amazon_region
        
        if not tag:
            # Return basic Amazon link if no affiliate tag
            return f"https://amazon.{region}/dp/{asin}/"
        
        url = f"https://amazon.{region}/dp/{asin}/?tag={tag}"
        return url
    
    def generate_aliexpress_link(self, product_id, affiliate_id=None):
        """
        Generate AliExpress affiliate link
        
        Note: AliExpress requires specific affiliate program setup
        This is a basic template
        """
        
        if not product_id:
            return None
        
        # Basic AliExpress link (without affiliate tracking)
        url = f"https://www.aliexpress.com/item/{product_id}.html"
        return url
    
    def generate_custom_tracking_link(self, url, source, medium, campaign):
        """
        Add UTM parameters for tracking
        
        Args:
            url: Base URL
            source: Traffic source (tiktok, instagram, youtube)
            medium: Medium (video, social)
            campaign: Campaign name
        
        Returns:
            URL with UTM parameters
        """
        
        params = {
            'utm_source': source,
            'utm_medium': medium,
            'utm_campaign': campaign,
        }
        
        separator = '&' if '?' in url else '?'
        tracking_url = url + separator + urlencode(params)
        
        return tracking_url
    
    def shorten_url(self, url, service='bit.ly'):
        """
        Shorten URL (basic implementation)
        
        Note: Requires API keys for actual shortening services
        """
        
        # This would require integration with a URL shortening service
        # For now, return original URL
        return url
