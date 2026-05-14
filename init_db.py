#!/usr/bin/env python
"""Initialize database and create sample data"""

import os
from app import create_app, db
from app.models import Product

def init_database():
    """Initialize database"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created")
        
        # Add sample products if none exist
        if Product.query.first() is None:
            sample_products = [
                {
                    'name': 'Wireless Bluetooth Headphones',
                    'description': 'High-quality wireless headphones with noise cancellation',
                    'price': 29.99,
                    'image_url': 'https://via.placeholder.com/500x500?text=Headphones',
                    'amazon_asin': 'B08EXAMPLE1',
                    'category': 'Electronics'
                },
                {
                    'name': 'USB-C Fast Charger',
                    'description': '65W USB-C fast charger compatible with all devices',
                    'price': 19.99,
                    'image_url': 'https://via.placeholder.com/500x500?text=Charger',
                    'amazon_asin': 'B08EXAMPLE2',
                    'category': 'Electronics'
                },
                {
                    'name': 'Phone Stand Mount',
                    'description': 'Adjustable phone stand for desk and car',
                    'price': 12.99,
                    'image_url': 'https://via.placeholder.com/500x500?text=Phone+Stand',
                    'amazon_asin': 'B08EXAMPLE3',
                    'category': 'Accessories'
                },
            ]
            
            for product_data in sample_products:
                product = Product(**product_data)
                db.session.add(product)
            
            db.session.commit()
            print(f"✓ Added {len(sample_products)} sample products")
        
        # Create upload folders
        os.makedirs('uploads', exist_ok=True)
        os.makedirs('videos', exist_ok=True)
        os.makedirs('temp', exist_ok=True)
        print("✓ Created folders: uploads, videos, temp")
        
        print("\n✅ Database initialization complete!")
        print("\nNext steps:")
        print("1. Create .env file from .env.example")
        print("2. Add your API keys (GROQ_API_KEY, AMAZON_AFFILIATE_ID)")
        print("3. Run: python app.py")
        print("4. Visit: http://localhost:5000")

if __name__ == '__main__':
    init_database()
