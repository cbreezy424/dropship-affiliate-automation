import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import json
from typing import List, Dict

class ProductScraper:
    """Service for scraping products from AliExpress, Amazon, eBay"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.categories = {
            'health': ['health', 'fitness', 'wellness', 'supplement', 'yoga', 'meditation'],
            'wealth': ['investment', 'course', 'book', 'passive income', 'business'],
            'wellness': ['beauty', 'skincare', 'sleep', 'nutrition', 'mental health']
        }
    
    def scrape_aliexpress_products(self, category='health', limit=20):
        """
        Scrape trending products from AliExpress
        
        Args:
            category: health, wealth, or wellness
            limit: Number of products to scrape
        
        Returns:
            List of product dictionaries
        """
        
        products = []
        keywords = self.categories.get(category, ['health'])
        
        try:
            for keyword in keywords[:3]:  # Search 3 keywords
                url = f"https://www.aliexpress.com/wholesale?SearchText={keyword}&SortType=best_sales"
                
                try:
                    response = requests.get(url, headers=self.headers, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract product data (simplified - actual implementation would be more robust)
                    product_items = soup.find_all('div', class_='organic-list-offer')[:limit]
                    
                    for item in product_items:
                        try:
                            name = item.find('h2')
                            price = item.find('span', class_='price')
                            rating = item.find('span', class_='rate')
                            
                            if name and price:
                                product = {
                                    'name': name.text.strip(),
                                    'price': float(price.text.strip().replace('$', '')),
                                    'rating': float(rating.text.split()[0]) if rating else 0,
                                    'category': category,
                                    'source': 'aliexpress',
                                    'aliexpress_url': item.find('a')['href'] if item.find('a') else ''
                                }
                                products.append(product)
                        except (ValueError, AttributeError, TypeError):
                            continue
                
                except requests.RequestException as e:
                    print(f"Error scraping AliExpress: {str(e)}")
                    continue
                
                time.sleep(2)  # Rate limiting
        
        except Exception as e:
            print(f"Error in AliExpress scraping: {str(e)}")
        
        return products[:limit]
    
    def scrape_amazon_products(self, category='health', limit=20):
        """
        Scrape products from Amazon
        
        Args:
            category: health, wealth, or wellness
            limit: Number of products
        
        Returns:
            List of product dictionaries
        """
        
        products = []
        keywords = self.categories.get(category, ['health'])
        
        try:
            for keyword in keywords[:3]:
                url = f"https://www.amazon.com/s?k={keyword}"
                
                try:
                    response = requests.get(url, headers=self.headers, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract product data
                    product_items = soup.find_all('div', {'data-component-type': 's-search-result'})[:limit]
                    
                    for item in product_items:
                        try:
                            name_tag = item.find('h2')
                            price_tag = item.find('span', class_='a-price-whole')
                            rating_tag = item.find('span', class_='a-star-small')
                            asin_tag = item.get('data-asin')
                            
                            if name_tag and price_tag:
                                product = {
                                    'name': name_tag.text.strip(),
                                    'price': float(price_tag.text.replace('$', '').replace(',', '')),
                                    'rating': float(rating_tag.text.split()[0]) if rating_tag else 0,
                                    'category': category,
                                    'source': 'amazon',
                                    'amazon_asin': asin_tag,
                                    'image_url': item.find('img')['src'] if item.find('img') else ''
                                }
                                products.append(product)
                        except (ValueError, AttributeError, TypeError):
                            continue
                
                except requests.RequestException as e:
                    print(f"Error scraping Amazon: {str(e)}")
                    continue
                
                time.sleep(2)
        
        except Exception as e:
            print(f"Error in Amazon scraping: {str(e)}")
        
        return products[:limit]
    
    def scrape_ebay_products(self, category='health', limit=20):
        """
        Scrape products from eBay
        
        Args:
            category: health, wealth, or wellness
            limit: Number of products
        
        Returns:
            List of product dictionaries
        """
        
        products = []
        keywords = self.categories.get(category, ['health'])
        
        try:
            for keyword in keywords[:3]:
                url = f"https://www.ebay.com/sch/i.html?_nkw={keyword}"
                
                try:
                    response = requests.get(url, headers=self.headers, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract product data
                    product_items = soup.find_all('div', class_='s-item')[:limit]
                    
                    for item in product_items:
                        try:
                            name_tag = item.find('div', class_='s-item__title')
                            price_tag = item.find('span', class_='s-item__price')
                            rating_tag = item.find('span', class_='clipped')
                            
                            if name_tag and price_tag:
                                product = {
                                    'name': name_tag.text.strip(),
                                    'price': float(price_tag.text.replace('$', '').split()[0]),
                                    'rating': float(rating_tag.text.split()[0]) if rating_tag else 0,
                                    'category': category,
                                    'source': 'ebay',
                                    'image_url': item.find('img')['src'] if item.find('img') else ''
                                }
                                products.append(product)
                        except (ValueError, AttributeError, TypeError):
                            continue
                
                except requests.RequestException as e:
                    print(f"Error scraping eBay: {str(e)}")
                    continue
                
                time.sleep(2)
        
        except Exception as e:
            print(f"Error in eBay scraping: {str(e)}")
        
        return products[:limit]
    
    def filter_quality_products(self, products, min_rating=3.5, min_price=5, max_price=200):
        """
        Filter products by quality criteria
        
        Args:
            products: List of products
            min_rating: Minimum rating (0-5)
            min_price: Minimum price
            max_price: Maximum price
        
        Returns:
            Filtered product list
        """
        
        filtered = []
        for product in products:
            if (product.get('rating', 0) >= min_rating and 
                min_price <= product.get('price', 0) <= max_price):
                filtered.append(product)
        
        # Sort by rating (descending)
        return sorted(filtered, key=lambda x: x.get('rating', 0), reverse=True)
    
    def scrape_all_categories(self, limit=50):
        """
        Scrape all categories and combine results
        
        Args:
            limit: Total products to scrape
        
        Returns:
            List of products from all sources
        """
        
        all_products = []
        
        # Scrape from each category
        for category in ['health', 'wealth', 'wellness']:
            print(f"\n📦 Scraping {category} products...")
            
            # Try each source
            try:
                products = self.scrape_aliexpress_products(category, limit // 3)
                all_products.extend(products)
            except Exception as e:
                print(f"AliExpress error: {e}")
            
            try:
                products = self.scrape_amazon_products(category, limit // 3)
                all_products.extend(products)
            except Exception as e:
                print(f"Amazon error: {e}")
            
            try:
                products = self.scrape_ebay_products(category, limit // 3)
                all_products.extend(products)
            except Exception as e:
                print(f"eBay error: {e}")
        
        # Filter quality products
        filtered = self.filter_quality_products(all_products)
        
        print(f"\n✓ Found {len(filtered)} quality products")
        return filtered[:limit]
    
    def get_sample_products(self):
        """
        Get sample products (fallback when scraping fails)
        
        Returns:
            List of sample products
        """
        
        sample_products = [
            {
                'name': 'Yoga Mat Premium Non-Slip',
                'price': 24.99,
                'rating': 4.7,
                'category': 'wellness',
                'source': 'aliexpress',
                'description': 'High-quality yoga mat for exercise and meditation'
            },
            {
                'name': 'Electric Massage Gun',
                'price': 39.99,
                'rating': 4.5,
                'category': 'health',
                'source': 'amazon',
                'amazon_asin': 'B08EXAMPLE',
                'description': 'Portable muscle recovery massage device'
            },
            {
                'name': 'Meditation Cushion Zafu',
                'price': 34.99,
                'rating': 4.6,
                'category': 'wellness',
                'source': 'ebay',
                'description': 'Comfortable meditation and yoga cushion'
            },
            {
                'name': 'Portable Water Bottle 1L',
                'price': 14.99,
                'rating': 4.8,
                'category': 'health',
                'source': 'aliexpress',
                'description': 'Eco-friendly reusable water bottle'
            },
            {
                'name': 'Online Business Course Bundle',
                'price': 49.99,
                'rating': 4.4,
                'category': 'wealth',
                'source': 'amazon',
                'description': 'Complete guide to starting an online business'
            },
        ]
        
        return sample_products
