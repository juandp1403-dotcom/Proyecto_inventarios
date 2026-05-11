from app import create_app
from init_db import init_database
import os

os.makedirs('instance', exist_ok=True)

app = create_app()

if __name__ == '__main__':
    init_database(app)

    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
