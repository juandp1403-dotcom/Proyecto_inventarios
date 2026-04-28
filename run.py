from app import create_app
from init_db import init_database

init_database()

app = create_app()

if __name__ == '__main__':
    debug_mode = True if __import__('os').getenv('FLASK_ENV') == 'development' else False
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)