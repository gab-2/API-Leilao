from flask import Flask
from routes import setup_routes
from database import init_db
import os

app = Flask(__name__)
setup_routes(app)
init_db(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
