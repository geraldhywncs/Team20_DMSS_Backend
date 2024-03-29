from flask import jsonify
from config.database_config import db
from model.category_model import Category_Model

class Category_Utility:
    def __init__(self, app):
        self.app = app

    def read_category(self, data):
        try:
            user_id = data.get('user_id')
            if user_id is not None:
                categories = Category_Model.query.filter_by(user_id=user_id).all()
                if categories:  
                    categories_list = [{'category_id': category.category_id, 'category_name': category.category_name, 'user_id': category.user_id} for category in categories]
                    return jsonify(categories=categories_list, status_code="200")
                else:
                    return jsonify(message=f'Category with user id {user_id} not found', status_code="404"), 404
            else:
                categories = Category_Model.query.all()
                if categories:
                    categories_list = [{'category_id': category.category_id, 'category_name': category.category_name, 'user_id': category.user_id} for category in categories]
                    return jsonify(categories=categories_list)
                else:
                    return jsonify(message=f'Categories are not found'), 404
                
        except Exception as e:
            return jsonify(message=f'Error reading categories: {str(e)}', status_code="500"), 500

    def add_category(self, data):
        category_name = data.get('category_name')
        user_id = data.get('user_id')

        if not category_name or not user_id:
            return jsonify({'error': 'Category name and user ID are required', 'status_code': 400}), 400

        existing_category = Category_Model.query.filter_by(category_name=category_name, user_id=user_id).first()
        if existing_category:
            return jsonify({'error': 'Category already exists for this user', 'status_code': 409}), 409

        new_category = Category_Model(category_name=category_name, user_id=user_id)
        db.session.add(new_category)
        db.session.commit()

        return jsonify({'message': 'Category added successfully','category_name': category_name, 'status_code': 200}), 200

    def delete_category(self, data):
        category_id = data.get('category_id')
        user_id = data.get('user_id')

        if not category_id or not user_id:
            return jsonify({'error': 'Category ID and user ID are required', 'status_code': 400}), 400

        category_to_delete = Category_Model.query.filter_by(category_id=category_id, user_id=user_id).first()

        if not category_to_delete:
            return jsonify({'error': 'Category not found', 'status_code': 404}), 404

        db.session.delete(category_to_delete)
        db.session.commit()

        return jsonify({'message': 'Category deleted successfully', 'status_code': 200}), 200

