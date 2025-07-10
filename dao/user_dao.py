from db import db
from models.user import User

class UserDAO:
    def create_user(self, user):
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            return None
    
    def get_user_by_id(self, user_id):
        return User.query.get(user_id)
    
    def get_user_by_username(self, username):
        return User.query.filter_by(username=username).first()
    
    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()
    
    def update_user(self, user):
        try:
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            print(f"Error updating user: {e}")
            return None
    
    def delete_user(self, user_id):
        try:
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting user: {e}")
            return False
    
    def get_all_users(self, page=1, per_page=10):
        return User.query.paginate(page=page, per_page=per_page, error_out=False)