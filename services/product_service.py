from app.models import Product
from app import db
from app.utils import generate_slug

class ProductService:
    """Service for managing products"""
    
    def create_product(self, name, description, price, image_url, amazon_asin=None, aliexpress_url=None, category=None):
        """Create new product"""
        product = Product(
            name=name,
            description=description,
            price=price,
            image_url=image_url,
            amazon_asin=amazon_asin,
            aliexpress_url=aliexpress_url,
            category=category,
            slug=generate_slug(name)
        )
        db.session.add(product)
        db.session.commit()
        return product
    
    def get_product(self, product_id):
        """Get product by ID"""
        return Product.query.get(product_id)
    
    def get_all_products(self):
        """Get all products"""
        return Product.query.all()
    
    def update_product(self, product_id, **kwargs):
        """Update product"""
        product = Product.query.get(product_id)
        if product:
            for key, value in kwargs.items():
                if hasattr(product, key) and value is not None:
                    setattr(product, key, value)
            db.session.commit()
        return product
    
    def delete_product(self, product_id):
        """Delete product"""
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
        return True
    
    def search_products(self, query):
        """Search products by name or description"""
        return Product.query.filter(
            (Product.name.ilike(f'%{query}%')) |
            (Product.description.ilike(f'%{query}%'))
        ).all()
