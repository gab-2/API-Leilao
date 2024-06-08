from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    app.config.from_object('config.Config')
    db.init_app(app)
    with app.app_context():
        db.create_all()

# Definindo Base para ser usada nos modelos
Base = db.Model
db_session = db.session
