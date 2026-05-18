from flask import Flask, render_template, redirect, url_for, session, request, g
from dotenv import load_dotenv
import logging
import atexit
import json
import os

# Import the blueprint
from main_routes import bp

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

handlers = [logging.StreamHandler(), logging.FileHandler('logs.log')]
formatter = logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

for handler in handlers:
    handler.setLevel('DEBUG')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

app = Flask(__name__)
logger.info("Website is live")


def app_shutdown():
    logger.info("Website is shut down")


atexit.register(app_shutdown)

load_dotenv('.env')
app.secret_key = os.getenv('SECRET_KEY')

# Register the blueprint
app.register_blueprint(bp)

# Language options (only needed here for root redirect)
LANGUAGE_OPTIONS = {
    'pl': {'name': 'Polski'},
    'en': {'name': 'English'},
    'de': {'name': 'Deutsch'},
    'ukr': {'name': 'Українська'},
    'ja': {'name': '日本語'}
}


def load_translations(lang_code):
    file_path = f"translations/{lang_code}.json"
    if not os.path.exists(file_path):
        file_path = "translations/pl.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# Global context processor
@app.context_processor
def inject_translations():
    lang = getattr(g, 'lang_code', session.get('lang', 'pl'))
    translations = load_translations(lang)
    return dict(translations=translations, lang=lang, language_options=LANGUAGE_OPTIONS)


# Root route - redirects to appropriate language version
@app.route('/')
def root():
    lang = session.get('lang')
    if not lang:
        best_match = request.accept_languages.best_match(['pl', 'en', 'de', 'ukr', 'ja'])
        lang = best_match if best_match else 'pl'
    session['lang'] = lang
    return redirect(url_for('main.index', lang_code=lang))


# FIXED: Language switcher endpoint (matches the form action)


@app.after_request
def add_header(response):
    if (request.path.startswith('/static/') or
            request.path.endswith(('.webp', '.jpg', '.jpeg', '.png', '.css', '.js', '.mp4', '.webm'))):
        response.cache_control.max_age = 31536000
        response.cache_control.public = True
        if 'v=' in request.path or '.min.' in request.path:
            response.cache_control.immutable = True
    return response


if __name__ == '__main__':
    app.run()