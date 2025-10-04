# src/poject/api/app.py
import os
from pathlib import Path
from flask import Flask, render_template
from .routes import bp
from ..config.settings import settings

def create_app():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base_dir, "templates")
    app = Flask(__name__, template_folder=template_dir)
    app.register_blueprint(bp, url_prefix="/api")
    app.config["DEBUG"] = settings.DEBUG



    @app.route("/")
    def index():
        return render_template("index.html")

    return app

# Variable pour gunicorn
app = create_app()
