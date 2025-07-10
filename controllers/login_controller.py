from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from models.user import User
from dao.user_dao import UserDAO

login_bp = Blueprint('login', __name__)
user_dao = UserDAO()

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please fill in all fields', 'error')
            return render_template('login.html')
        
        user = user_dao.get_user_by_username(username)
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')