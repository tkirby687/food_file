from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session, redirect
from flask_app.models import user


class Item:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.qty = data['qty']
        self.date_requested = data['date_requested']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
        
    # Class method to Create
    @classmethod
    def create_item(cls, form_data):
        query = "INSERT INTO items (name, description, qty, date_requested, user_id) VALUES (%(name)s, %(description)s, %(qty)s, %(date_requested)s, %(user_id)s);"
        return connectToMySQL('solo_project_schema').query_db(query, form_data)
    
    # Class method to Retrieve (all) items
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM items;"
        results = connectToMySQL('solo_project_schema').query_db(query)
        items = []
        for item in results:
            items.append( cls(items) )
        return items
    
    # Method to Retrieve items with user data
    @classmethod
    def get_all_items_with_user(cls):
        query = "SELECT * FROM items LEFT JOIN users on items.user_id = users.id;"
        items = connectToMySQL('solo_project_schema').query_db(query)
        results = []
        for item in items:
            data = {
                'id' : item['users.id'],
                'first_name' : item['first_name'],
                'last_name' : item['last_name'],
                'email' : item['email'],
                'pwd' : item['pwd'],
                'created_at' : item['users.created_at'],
                'updated_at' : item['users.updated_at']
            }
            one_item = cls(item)
            one_item.creator = user.User(data)
            results.append(one_item) 
        return items
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM items LEFT JOIN users on items.user_id = users.id WHERE items.id = %(id)s;"
        result = connectToMySQL("solo_project_schema").query_db(query,data)
        result = result[0]
        item = cls(result)
        item.user = user.User(
                {
                    "id": result["user_id"],
                    "first_name": result["first_name"],
                    "last_name": result["last_name"],
                    "email": result["email"],
                    "pwd" : result["pwd"],
                    "created_at": result["created_at"],
                    "updated_at": result["updated_at"]
                }
            )
        return item
    
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM items WHERE id = %(id)s;"
        results = connectToMySQL('solo_project_schema').query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def update_item(cls, form_data):
        query = "UPDATE items SET name=%(name)s, description=%(description)s, qty=%(qty)s, date_requested=%(date_requested)s WHERE id=%(id)s;"
        return connectToMySQL('solo_project_schema').query_db(query, form_data)
    
    @classmethod
    def delete_item(cls, data):
        
        one_item = cls.get_one(data)
        if session['user_id'] != one_item.user_id:
            session.clear()    
            return redirect('/')
        
        query = "DELETE FROM items WHERE id=%(id)s;"
        return connectToMySQL('solo_project_schema').query_db(query, data)
    
    @classmethod
    def delete_all(cls):
        
        if 'user_id' not in session:
            session.clear()
            return redirect('/')
        query = "DELETE FROM items;"
        return connectToMySQL('solo_project_schema').query_db(query)
        
    
    @staticmethod
    def item_validator(data):
        
        is_valid = True
        
        if len(data["name"]) < 3:
            is_valid = False
            flash("Item must be at least 3 characters.")
        if len(data["description"]) < 3:
            is_valid = False
            flash("Description must be at least 3 characters.")
        if data['qty'] == '':
            is_valid = False
            flash("Quantity is required.")
        elif int(data['qty']) < 1:
            flash("Must be min 1 quantity.")
            is_valid = False
        if data['date_requested'] == '':
            is_valid = False
            flash("Date requested is required.")
            
        return is_valid
    
   