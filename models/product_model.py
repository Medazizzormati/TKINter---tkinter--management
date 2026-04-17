from database import Database







class ProductModel:



    def __init__(self):



        self.db = Database()







    def create(self, category_id, name, price, stock, image_url=None):



        query = "INSERT INTO products (category_id, name, price, stock, image_url) VALUES (%s, %s, %s, %s, %s)"



        params = (category_id, name, price, stock, image_url)



        return self.db.execute_query(query, params, commit=True)







    def get_all_with_category(self):



        query = """
            SELECT p.*, c.name as category_name 
            FROM products p 
            JOIN categories c ON p.category_id = c.id 
            ORDER BY p.id DESC
        """



        return self.db.fetch_all(query)







    def update(self, product_id, category_id, name, price, stock, image_url=None):



        query = "UPDATE products SET category_id = %s, name = %s, price = %s, stock = %s, image_url = %s WHERE id = %s"



        params = (category_id, name, price, stock, image_url, product_id)



        return self.db.execute_query(query, params, commit=True)







    def delete(self, product_id):



        query = "DELETE FROM products WHERE id = %s"



        return self.db.execute_query(query, (product_id,), commit=True)







    def search(self, term):



        query = """
            SELECT p.*, c.name as category_name 
            FROM products p 
            JOIN categories c ON p.category_id = c.id 
            WHERE p.name LIKE %s OR c.name LIKE %s
        """



        params = (f"%{term}%", f"%{term}%")



        return self.db.fetch_all(query, params)



    



    def get_stats(self):



        query = "SELECT COUNT(*) as total_count, SUM(stock) as total_stock, AVG(price) as avg_price FROM products"



        return self.db.fetch_one(query)







    def get_all_with_details(self):



                                                                  



        query = """
            SELECT p.id, p.name, p.price, p.stock, p.category_id, p.image_url, c.name as category_name
            FROM products p
            JOIN categories c ON p.category_id = c.id
            ORDER BY p.stock DESC
            LIMIT 15
        """



        return self.db.fetch_all(query)



