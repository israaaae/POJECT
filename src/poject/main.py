# src/main.py
from src.poject.api.app import create_app
from src.poject.config.settings import settings

app = create_app()

if __name__ == "__main__":
    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
