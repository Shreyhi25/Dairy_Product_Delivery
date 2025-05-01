import os
from backend.app import create_app

# Set the environment
env = os.getenv('FLASK_ENV', 'production')
app = create_app(config_name=env)

if __name__ == "__main__":
    app.run() 