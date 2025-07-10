from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.user import User
from dao.user_dao import UserDAO

register_bp = Blueprint('register', __name__)
user_dao = UserDAO()

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        # Validation
        if not all([username, email, password, confirm_password]):
            flash('Please fill in all required fields', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if user_dao.get_user_by_username(username):
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if user_dao.get_user_by_email(email):
            flash('Email already exists', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            phone=phone,
            address=address
        )
        user.set_password(password)
        
        if user_dao.create_user(user):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login.login'))
        else:
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('register.html')