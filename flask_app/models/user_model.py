from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#let's us create a new user into the database
    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO users (first_name, email, password)
        VALUES (%(first_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

#get all the users by email
    @classmethod
    def get_by_email(cls, data):
        query = """
        SELECT * FROM users WHERE email = %(email)s;
        """
        results =  connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        
        return cls(results[0])

#get all the users by id
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * FROM users WHERE id = %(id)s;
        """
        results =  connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        
        return cls(results[0])


    @staticmethod
    def validator(data):
        is_valid = True
    # First Name
        if len(data['first_name']) < 2:
            is_valid = False
            flash("First name must be at least 2 characters", 'reg_name')
    # Email
        if len(data['email']) < 1:
            is_valid = False
            flash("Valid Email Required", 'reg_email')
        elif not EMAIL_REGEX.match(data['email']): #is the email valid regex
            flash('Invalid Email', 'reg_email')
        else: #is the email unique
            user_data = { #use a unique variable name
                'email': data['email']
            }
            potential_user = User.get_by_email(user_data)
            if potential_user: #if we did get a user back
                is_valid = False
                flash("Email already taken", 'reg_email')
    # Password
        if len(data['password']) < 8: #looks at the data from request.form
            is_valid = False
            flash("Password must be at least 8 characters", 'reg_password')
    # Confirm Password
        elif not data['password'] == data['confirm_pass']:
            is_valid = False
            flash("Passwords don't match", 'reg_confirm_pass')
    # Checkbox (I may want to add a date box and have this required for being under the age of 13 that a parent/guardian knows about this account on the internet)
        # if "checkbox" not in data:
        #     is_valid = False
        #     flash("Must Check Box", 'checkbox')

        return is_valid
