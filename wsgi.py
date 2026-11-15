"""WSGI entry point for Gunicorn or another production server."""

from dotenv import load_dotenv

from app import create_app

load_dotenv()
app = create_app()
