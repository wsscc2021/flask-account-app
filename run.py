#Application modules
from app import create_app
from config import DevelopmentConfig, ProductionConfig

app = create_app()

if __name__ == "__main__":
    RUN_OPTIONS = {"host": "0.0.0.0", "port": 5000, "threaded": True}
    app.run(**RUN_OPTIONS)