from database import Database

class CategoryModel:
    def __init__(self):
        self.db = Database()

    def create(self, name, description):
        query = "INSERT INTO categories (name, description) VALUES (%s, %s)"
        params = (name, description)
        return self.db.execute_query(
            query, params, commit=True
            )

    def get_all(self):
        query = "SELECT * FROM categories ORDER BY name ASC"
        return self.db.fetch_all(query)

    def get_by_id(self, category_id):
        query = "SELECT * FROM categories WHERE id = %s"
        return self.db.fetch_one(query, (category_id,))

    def update(self, category_id, name, description):
        query = "UPDATE categories SET name = %s, description = %s WHERE id = %s"
        params = (name, description, category_id)
        return self.db.execute_query(query, params, commit=True)

    def delete(self, category_id):
        query = "DELETE FROM categories WHERE id = %s"
        return self.db.execute_query(query, (category_id,), commit=True)

    def search(self, term):
        query = "SELECT * FROM categories WHERE name LIKE %s OR description LIKE %s"
        params = (f"%{term}%", f"%{term}%")
        return self.db.fetch_all(query, params)

    def get_all_with_product_count(self):
        """Get all categories with product counts for dashboard"""
        query = """
            SELECT c.id, c.name, c.description, COUNT(p.id) as product_count
            FROM categories c
            LEFT JOIN products p ON c.id = p.category_id
            GROUP BY c.id, c.name, c.description
            ORDER BY COUNT(p.id) DESC
        """
        return self.db.fetch_all(query)
