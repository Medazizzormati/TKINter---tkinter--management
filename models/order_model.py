from database import Database







class OrderModel:



    def __init__(self):



        self.db = Database()







    def create(self, product_id, customer_name, quantity, total_price):



        query = "INSERT INTO orders (product_id, customer_name, quantity, total_price) VALUES (%s, %s, %s, %s)"



        params = (product_id, customer_name, quantity, total_price)



        return self.db.execute_query(query, params, commit=True)







    def get_all_with_product(self):



        query = """
            SELECT o.*, p.name as product_name 
            FROM orders o 
            JOIN products p ON o.product_id = p.id 
            ORDER BY o.order_date DESC
        """



        return self.db.fetch_all(query)







    def get_stats(self):



        query = "SELECT COUNT(*) as order_count, SUM(total_price) as total_revenue FROM orders"



        return self.db.fetch_one(query)







    def get_by_customer(self, customer_name):



                                                                           



        query = """
            SELECT o.*, p.name as product_name 
            FROM orders o 
            JOIN products p ON o.product_id = p.id 
            WHERE o.customer_name = %s
            ORDER BY o.order_date DESC
        """



        return self.db.fetch_all(query, (customer_name,))







    def update_status(self, order_id, status):



                                                                              



        query = "UPDATE orders SET status = %s WHERE id = %s"



        return self.db.execute_query(query, (status, order_id), commit=True)







    def delete(self, order_id):



        query = "DELETE FROM orders WHERE id = %s"



        return self.db.execute_query(query, (order_id,), commit=True)



