-- Comprehensive Supermarket Sample Data for Smart Management System

USE smart_management_system;

-- Default Admin User (password: admin123 - hashed SHA256)
INSERT INTO users (username, email, password, role) VALUES 
('admin', 'admin@supermarket.local', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin')
ON DUPLICATE KEY UPDATE role='admin', password='240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9';

-- Sample Supermarket Categories
INSERT IGNORE INTO categories (id, name, description) VALUES 
(1, 'Fruits & Vegetables', 'Fresh produce section'),
(2, 'Dairy & Eggs', 'Milk, cheese, yogurt, and eggs'),
(3, 'Meat & Seafood', 'Fresh meat, poultry, and seafood'),
(4, 'Bakery', 'Bread, pastries, and baked goods'),
(5, 'Beverages', 'Coffee, tea, juice, and soft drinks'),
(6, 'Pantry Staples', 'Rice, pasta, flour, and grains'),
(7, 'Snacks & Sweets', 'Chips, cookies, and confectionery'),
(8, 'Frozen Foods', 'Frozen vegetables, meals, and ice cream'),
(9, 'Personal Care', 'Soap, shampoo, toothpaste'),
(10, 'Household Items', 'Cleaning supplies and essentials');

-- Fruits & Vegetables Products
INSERT IGNORE INTO products (category_id, name, price, stock, image_url) VALUES 
(1, 'Fresh Apples', 3.99, 150, 'assets/catalog_images/apples.png'),
(1, 'Organic Bananas', 2.49, 200, 'assets/catalog_images/bananas.png'),
(1, 'Carrots (1kg)', 1.99, 100, 'assets/catalog_images/carrots.png'),
(1, 'Broccoli', 3.49, 85, 'assets/catalog_images/broccoli.png'),
(1, 'Tomatoes', 4.99, 120, 'assets/catalog_images/tomatoes.png');

-- Dairy & Eggs Products
INSERT IGNORE INTO products (category_id, name, price, stock, image_url) VALUES 
(2, 'Whole Milk (1L)', 3.29, 200, 'assets/catalog_images/milk.png'),
(2, 'Cheddar Cheese', 7.99, 85, 'assets/catalog_images/cheddar.png'),
(2, 'Eggs (Dozen)', 4.99, 250, 'assets/catalog_images/eggs.png'),
(2, 'Cream Cheese', 4.99, 60, 'assets/catalog_images/cream_cheese.png');

-- Meat & Seafood Products
INSERT IGNORE INTO products (category_id, name, price, stock, image_url) VALUES 
(3, 'Chicken Breast', 9.99, 120, 'assets/catalog_images/chicken.png'),
(3, 'Ground Beef', 8.49, 95, 'assets/catalog_images/beef.png'),
(3, 'Salmon Fillet', 14.99, 45, 'assets/catalog_images/salmon.png');

-- Bakery Products
INSERT IGNORE INTO products (category_id, name, price, stock, image_url) VALUES 
(4, 'Whole Wheat Bread', 3.49, 60, 'assets/catalog_images/bread.png'),
(4, 'Croissants', 5.99, 50, 'assets/catalog_images/croissants.png'),
(4, 'Chocolate Chip Cookies', 4.99, 70, 'assets/catalog_images/cookies.png'),
(4, 'Baguette', 3.99, 50, 'assets/catalog_images/baguette.png');

-- Beverages
INSERT IGNORE INTO products (category_id, name, price, stock, image_url) VALUES 
(5, 'Orange Juice', 4.49, 100, 'assets/catalog_images/orange_juice.png'),
(5, 'Coffee Beans', 8.99, 75, 'assets/catalog_images/coffee_beans.png'),
(5, 'Green Tea', 5.99, 60, 'assets/catalog_images/green_tea.png');

-- Pantry Staples
INSERT IGNORE INTO products (category_id, name, price, stock, image_url) VALUES 
(6, 'Jasmine Rice', 6.99, 100, 'assets/catalog_images/jasmine_rice.png'),
(6, 'Pasta', 1.99, 250, 'assets/catalog_images/pasta.png'),
(6, 'Olive Oil', 9.99, 50, 'assets/catalog_images/olive_oil.png');

-- Snacks & Sweets
INSERT IGNORE INTO products (category_id, name, price, stock, image_url) VALUES 
(7, 'Potato Chips', 3.49, 120, 'assets/catalog_images/potato_chips.png'),
(7, 'Chocolate Bar', 1.99, 200, 'assets/catalog_images/chocolate_bar.png');

-- Household Items
INSERT IGNORE INTO products (category_id, name, price, stock, image_url) VALUES 
(10, 'Laundry Detergent', 9.99, 80, 'assets/catalog_images/detergent.png'),
(10, 'Dish Soap', 2.99, 150, 'assets/catalog_images/dish_soap.png');
