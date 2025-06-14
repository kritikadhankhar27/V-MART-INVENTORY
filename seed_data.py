from app import db
from models import Product
import logging

def seed_database():
    """Seed the database with initial grocery store inventory"""
    
    # Check if products already exist
    if Product.query.count() > 0:
        logging.info("Database already has products, skipping seed")
        return
    
    # Grocery store products with real data
    products_data = [
        # Fruits
        {"name": "Red Apples", "description": "Fresh, crisp red apples perfect for snacking", "category": "Fruits", "price": 2.99, "quantity": 150, "min_stock_level": 20, "barcode": "1234567890001", "image_url": "https://pixabay.com/get/gfe0e5dd8209387f9df798bb6bb7586bed79f682dd8ec25dac41bf02a2ccec68b241d8be72e344d6f28ead3bf716ecf92071d27569cabcf45b806b51e78fa1451_1280.jpg"},
        {"name": "Bananas", "description": "Yellow, ripe bananas rich in potassium", "category": "Fruits", "price": 1.49, "quantity": 200, "min_stock_level": 30, "barcode": "1234567890002", "image_url": "https://pixabay.com/get/g4b012402dcd8a4cb3ab735807848478b657565b54ba50dc9c72b0acda63c8b250b72082e8256e2dbb181361d3b9820db42bf298ae2d21e27ee72525c3d2c2b62_1280.jpg"},
        {"name": "Oranges", "description": "Juicy Valencia oranges packed with Vitamin C", "category": "Fruits", "price": 3.49, "quantity": 120, "min_stock_level": 25, "barcode": "1234567890003", "image_url": "https://pixabay.com/get/g853f129a89aec927fb3b51bc00bc30d34fc8ede1942bc931516bc84838729b6968e9374da6008dcb653a7ec604ad6e5d22a5d06b15576cd29838e1c42d472846_1280.jpg"},
        {"name": "Green Grapes", "description": "Sweet and seedless green grapes", "category": "Fruits", "price": 4.99, "quantity": 80, "min_stock_level": 15, "barcode": "1234567890004"},
        {"name": "Strawberries", "description": "Fresh, red strawberries perfect for desserts", "category": "Fruits", "price": 5.99, "quantity": 60, "min_stock_level": 10, "barcode": "1234567890005"},
        {"name": "Pineapple", "description": "Sweet, tropical pineapple", "category": "Fruits", "price": 4.49, "quantity": 40, "min_stock_level": 8, "barcode": "1234567890006"},
        {"name": "Mangoes", "description": "Ripe, sweet mangoes", "category": "Fruits", "price": 2.99, "quantity": 55, "min_stock_level": 12, "barcode": "1234567890007"},
        {"name": "Avocados", "description": "Fresh Hass avocados", "category": "Fruits", "price": 1.99, "quantity": 90, "min_stock_level": 20, "barcode": "1234567890008"},
        
        # Vegetables
        {"name": "Carrots", "description": "Fresh orange carrots, great for cooking", "category": "Vegetables", "price": 1.99, "quantity": 180, "min_stock_level": 25, "barcode": "1234567890009", "image_url": "https://pixabay.com/get/gce9382bdc2448ad7192c2a43dd71ed952412d93f88de81ecb240433640ffeb96f63fae450d069756d81d41e057db91eb083e88866439bf67f992cf238f004658_1280.jpg"},
        {"name": "Broccoli", "description": "Fresh green broccoli crowns", "category": "Vegetables", "price": 2.49, "quantity": 75, "min_stock_level": 15, "barcode": "1234567890010"},
        {"name": "Bell Peppers", "description": "Colorful bell peppers - red, yellow, green", "category": "Vegetables", "price": 3.99, "quantity": 100, "min_stock_level": 20, "barcode": "1234567890011"},
        {"name": "Spinach", "description": "Fresh baby spinach leaves", "category": "Vegetables", "price": 2.99, "quantity": 65, "min_stock_level": 12, "barcode": "1234567890012", "image_url": "https://pixabay.com/get/g0a2077d9d82ac4aa7d2a87dd07c26350ff7cae61b2ee3a86020b9cadb8dd51148671bcca8b339aa130a530adad9344f14ca94ac429b4fcee76bf9bd6df93e36f_1280.jpg"},
        {"name": "Tomatoes", "description": "Ripe red tomatoes", "category": "Vegetables", "price": 2.79, "quantity": 140, "min_stock_level": 25, "barcode": "1234567890013"},
        {"name": "Cucumbers", "description": "Fresh green cucumbers", "category": "Vegetables", "price": 1.79, "quantity": 110, "min_stock_level": 20, "barcode": "1234567890014"},
        {"name": "Onions", "description": "Yellow cooking onions", "category": "Vegetables", "price": 1.49, "quantity": 200, "min_stock_level": 30, "barcode": "1234567890015"},
        {"name": "Potatoes", "description": "Russet potatoes perfect for baking", "category": "Vegetables", "price": 2.99, "quantity": 250, "min_stock_level": 40, "barcode": "1234567890016", "image_url": "https://pixabay.com/get/g0671a2f4a417b06cd6a3b3faa06f5ec6ce7c259db7735f82571f0bbf88c1c5363af6016cbe70952f7f8e789063103172f0a6b5970f819578999343798ab74144_1280.jpg"},
        
        # Dairy
        {"name": "Whole Milk", "description": "Fresh whole milk, 1 gallon", "category": "Dairy", "price": 3.49, "quantity": 85, "min_stock_level": 20, "barcode": "1234567890017"},
        {"name": "Greek Yogurt", "description": "Plain Greek yogurt, high in protein", "category": "Dairy", "price": 5.99, "quantity": 60, "min_stock_level": 15, "barcode": "1234567890018"},
        {"name": "Cheddar Cheese", "description": "Sharp cheddar cheese block", "category": "Dairy", "price": 4.99, "quantity": 45, "min_stock_level": 10, "barcode": "1234567890019"},
        {"name": "Butter", "description": "Unsalted butter, 1 lb", "category": "Dairy", "price": 4.49, "quantity": 70, "min_stock_level": 15, "barcode": "1234567890020"},
        {"name": "Eggs", "description": "Large brown eggs, dozen", "category": "Dairy", "price": 2.99, "quantity": 120, "min_stock_level": 25, "barcode": "1234567890021"},
        {"name": "Cream Cheese", "description": "Philadelphia cream cheese", "category": "Dairy", "price": 2.49, "quantity": 35, "min_stock_level": 8, "barcode": "1234567890022"},
        
        # Meat & Seafood
        {"name": "Chicken Breast", "description": "Boneless, skinless chicken breast", "category": "Meat & Seafood", "price": 8.99, "quantity": 50, "min_stock_level": 10, "barcode": "1234567890023"},
        {"name": "Ground Beef", "description": "85% lean ground beef", "category": "Meat & Seafood", "price": 6.99, "quantity": 40, "min_stock_level": 8, "barcode": "1234567890024"},
        {"name": "Salmon Fillet", "description": "Fresh Atlantic salmon fillet", "category": "Meat & Seafood", "price": 12.99, "quantity": 25, "min_stock_level": 5, "barcode": "1234567890025"},
        {"name": "Pork Chops", "description": "Bone-in pork chops", "category": "Meat & Seafood", "price": 7.99, "quantity": 30, "min_stock_level": 6, "barcode": "1234567890026"},
        
        # Beverages
        {"name": "Orange Juice", "description": "Fresh squeezed orange juice", "category": "Beverages", "price": 4.99, "quantity": 80, "min_stock_level": 15, "barcode": "1234567890027"},
        {"name": "Coffee Beans", "description": "Arabica coffee beans, medium roast", "category": "Beverages", "price": 12.99, "quantity": 45, "min_stock_level": 10, "barcode": "1234567890028"},
        {"name": "Green Tea", "description": "Organic green tea bags", "category": "Beverages", "price": 6.99, "quantity": 55, "min_stock_level": 12, "barcode": "1234567890029"},
        {"name": "Sparkling Water", "description": "Lemon flavored sparkling water", "category": "Beverages", "price": 3.99, "quantity": 100, "min_stock_level": 20, "barcode": "1234567890030"},
        
        # Pantry/Packaged Goods
        {"name": "Pasta", "description": "Whole wheat spaghetti", "category": "Pantry", "price": 1.99, "quantity": 150, "min_stock_level": 30, "barcode": "1234567890031", "image_url": "https://pixabay.com/get/g139056adc5d863284d9de6af75b2f05725d2415572ad64a58a85f0ee14a8ddcca9d9f76b2b2ef1b197dcf1ca60c929cfae8f153dd4cd831495d3cfe0ea73cb81_1280.jpg"},
        {"name": "Rice", "description": "Long grain white rice", "category": "Pantry", "price": 3.49, "quantity": 120, "min_stock_level": 25, "barcode": "1234567890032"},
        {"name": "Olive Oil", "description": "Extra virgin olive oil", "category": "Pantry", "price": 8.99, "quantity": 40, "min_stock_level": 8, "barcode": "1234567890033"},
        {"name": "Canned Tomatoes", "description": "Diced tomatoes in juice", "category": "Pantry", "price": 1.79, "quantity": 200, "min_stock_level": 40, "barcode": "1234567890034", "image_url": "https://pixabay.com/get/g8e549c7f2e2609137587166419d9203c8ee46a1269133d7b6d7726a33d618601c99964caeb2d4f76289572f86f782d9f5ec4f527c1b984aad552dfa9079362fc_1280.jpg"},
        {"name": "Black Beans", "description": "Canned black beans", "category": "Pantry", "price": 1.29, "quantity": 180, "min_stock_level": 35, "barcode": "1234567890035"},
        {"name": "Quinoa", "description": "Organic quinoa grain", "category": "Pantry", "price": 7.99, "quantity": 30, "min_stock_level": 6, "barcode": "1234567890036"},
        {"name": "Honey", "description": "Pure wildflower honey", "category": "Pantry", "price": 6.49, "quantity": 35, "min_stock_level": 7, "barcode": "1234567890037"},
        {"name": "Oats", "description": "Old fashioned rolled oats", "category": "Pantry", "price": 3.99, "quantity": 90, "min_stock_level": 18, "barcode": "1234567890038"},
        
        # Snacks
        {"name": "Almonds", "description": "Raw unsalted almonds", "category": "Snacks", "price": 8.99, "quantity": 50, "min_stock_level": 10, "barcode": "1234567890039"},
        {"name": "Granola Bars", "description": "Chewy granola bars variety pack", "category": "Snacks", "price": 4.99, "quantity": 75, "min_stock_level": 15, "barcode": "1234567890040"},
        {"name": "Pretzels", "description": "Traditional twisted pretzels", "category": "Snacks", "price": 2.99, "quantity": 85, "min_stock_level": 17, "barcode": "1234567890041"},
        {"name": "Trail Mix", "description": "Mixed nuts and dried fruit", "category": "Snacks", "price": 6.99, "quantity": 40, "min_stock_level": 8, "barcode": "1234567890042"},
        
        # Frozen Foods
        {"name": "Frozen Berries", "description": "Mixed berry blend", "category": "Frozen", "price": 4.99, "quantity": 60, "min_stock_level": 12, "barcode": "1234567890043"},
        {"name": "Frozen Pizza", "description": "Margherita frozen pizza", "category": "Frozen", "price": 5.99, "quantity": 45, "min_stock_level": 9, "barcode": "1234567890044"},
        {"name": "Ice Cream", "description": "Vanilla ice cream, 1.5 qt", "category": "Frozen", "price": 4.49, "quantity": 55, "min_stock_level": 11, "barcode": "1234567890045"},
        {"name": "Frozen Vegetables", "description": "Mixed vegetable medley", "category": "Frozen", "price": 2.99, "quantity": 80, "min_stock_level": 16, "barcode": "1234567890046"},
        
        # Bakery
        {"name": "Whole Wheat Bread", "description": "Fresh baked whole wheat bread", "category": "Bakery", "price": 2.99, "quantity": 70, "min_stock_level": 14, "barcode": "1234567890047"},
        {"name": "Bagels", "description": "Everything bagels, 6 pack", "category": "Bakery", "price": 3.99, "quantity": 50, "min_stock_level": 10, "barcode": "1234567890048"},
        {"name": "Croissants", "description": "Butter croissants, 4 pack", "category": "Bakery", "price": 4.99, "quantity": 35, "min_stock_level": 7, "barcode": "1234567890049"},
        {"name": "Muffins", "description": "Blueberry muffins, 6 pack", "category": "Bakery", "price": 5.99, "quantity": 40, "min_stock_level": 8, "barcode": "1234567890050"},
        
        # Health & Personal Care
        {"name": "Multivitamins", "description": "Daily multivitamin supplements", "category": "Health", "price": 12.99, "quantity": 25, "min_stock_level": 5, "barcode": "1234567890051"},
        {"name": "Toothpaste", "description": "Fluoride toothpaste", "category": "Health", "price": 3.99, "quantity": 60, "min_stock_level": 12, "barcode": "1234567890052"},
        {"name": "Shampoo", "description": "Moisturizing shampoo", "category": "Health", "price": 6.99, "quantity": 45, "min_stock_level": 9, "barcode": "1234567890053"},
    ]
    
    try:
        for product_data in products_data:
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
        logging.info(f"Successfully seeded database with {len(products_data)} products")
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error seeding database: {str(e)}")
        raise e
