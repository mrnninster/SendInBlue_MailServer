from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config.from_object('mail_app.config.BaseConfig')
    
    # Pushing Application Context
    with app.app_context():

        from . import routes
        
    return app
