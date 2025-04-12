from flask import Flask
from app.routes import routes

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = 'change-this-secret'
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
