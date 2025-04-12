from flask import session, redirect, url_for

def is_logged_in():
    return session.get('logged_in', False)

def login_required(f):
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper
