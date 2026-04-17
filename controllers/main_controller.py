from models.category_model import CategoryModel



from models.product_model import ProductModel



from models.order_model import OrderModel



from models.user_model import UserModel







class MainController:



    def __init__(self):



        self.category_model = CategoryModel()



        self.product_model = ProductModel()



        self.order_model = OrderModel()



        self.user_model = UserModel()







                      



    def get_categories(self):



        return self.category_model.get_all()







    def add_category(self, name, description):



        if not name:



            return False, "Name is required"



        try:



            self.category_model.create(name, description)



            return True, "Category added successfully"



        except Exception as e:



            return False, str(e)







                     



    def get_products(self):



        return self.product_model.get_all_with_category()







    def add_product(self, category_id, name, price, stock, image_url=None):



        if not name or not category_id:



            return False, "Name and Category are required"



        try:



            self.product_model.create(category_id, name, price, stock, image_url)



            return True, "Product added successfully"



        except Exception as e:



            return False, str(e)







                     



    def get_dashboard_stats(self):



        prod_stats = self.product_model.get_stats()



        order_stats = self.order_model.get_stats()



        



        return {



            'total_products': prod_stats.get('total_count', 0) if prod_stats else 0,



            'total_stock': prod_stats.get('total_stock', 0) if prod_stats else 0,



            'total_orders': order_stats.get('order_count', 0) if order_stats else 0,



            'total_revenue': float(order_stats.get('total_revenue', 0) or 0) if order_stats else 0.0



        }







                                 



    def get_all_products(self):



                                                                      



        try:



            return self.product_model.get_all_with_details()



        except Exception:



            return []







                                            



    def get_all_categories(self):



                                                                         



        try:



            return self.category_model.get_all_with_product_count()



        except Exception:



            return []







                            



    def login(self, username, password):



                               



        user = self.user_model.authenticate(username, password)



        return user is not None, user







    def signup(self, username, email, password, role='client'):



                                     



        if not username or not email or not password:



            return False, "Username, email and password are required"







                                



        import re



        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):



            return False, "Please enter a valid email address"







                                      



        if len(password) < 8:



            return False, "Password must be at least 8 characters long"







        if not re.search(r'[A-Z]', password):



            return False, "Password must contain at least one uppercase letter"







        if not re.search(r'[a-z]', password):



            return False, "Password must contain at least one lowercase letter"







        if not re.search(r'[0-9]', password):



            return False, "Password must contain at least one number"







        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):



            return False, "Password must contain at least one special character"







        if self.user_model.username_exists(username):



            return False, "Username already exists"







        if self.user_model.email_exists(email):



            return False, "Email already exists"







        try:



            self.user_model.create(username, email, password, role)



            return True, "Account created successfully"



        except Exception as e:



            return False, str(e)



                   



    def get_customer_orders(self, username):



                                                      



        return self.order_model.get_by_customer(username)







    def update_order_status(self, order_id, status):



                                           



        try:



            self.order_model.update_status(order_id, status)



            return True, "Order status updated"



        except Exception as e:



            return False, str(e)



