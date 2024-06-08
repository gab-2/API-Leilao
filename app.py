from flask import Flask
from routes import setup_routes
from database import init_db

app = Flask(__name__)
setup_routes(app)
init_db(app)

if __name__ == '__main__':
    app.run(debug=True)
