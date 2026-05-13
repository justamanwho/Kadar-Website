from flask import Flask, render_template, redirect, url_for, session, request
from dotenv import load_dotenv
import logging
import atexit
import json
import os


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
        file_path = "translations/pl.json"  # Default Language
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# 🔹 Global context processor so translations work in ALL templates (including base.html)
@app.context_processor
def inject_translations():
    lang = session.get('lang', 'pl')
    translations = load_translations(lang)
    return dict(translations=translations, lang=lang, language_options=LANGUAGE_OPTIONS)


@app.route('/')
def index():
    # --- Language logic ---
    if 'lang' not in session:
        session['lang'] = 'pl'  # Default Language

    max_length = max(len(option['name']) for option in LANGUAGE_OPTIONS.values())

    # --- Gallery logic ---
    gallery_path = os.path.join(app.static_folder, "gallery")
    files = sorted(os.listdir(gallery_path))

    gallery_files = []
    for f in files:
        # Skip WebP and already compressed videos
        if '_compressed' in f or f.lower().endswith('webp'):
            continue

        ext = f.lower().split('.')[-1]

        # Only include original images and videos
        if ext in ['jpg', 'jpeg', 'png', 'mp4', 'mov', 'webm']:
            gallery_files.append({
                "name": f,
                "is_video": ext in ["mp4", "mov", "webm"]
            })

    return render_template(
        'index.html',
        max_length=max_length,
        gallery_files=gallery_files
    )


@app.route('/<lang_code>')
def set_language(lang_code):
    if lang_code in LANGUAGE_OPTIONS:
        session['lang'] = lang_code
        logger.info(f"Language was set to {lang_code}")
    return redirect(url_for('index'))


@app.route('/credits')
def credits():
    max_length = max(len(option['name']) for option in LANGUAGE_OPTIONS.values())
    return render_template('credits.html', max_length=max_length)


@app.route('/kontakt')
def contact():
    max_length = max(len(option['name']) for option in LANGUAGE_OPTIONS.values())
    return render_template('contact.html', max_length=max_length)


@app.route('/o-nas')
def about():
    max_length = max(len(option['name']) for option in LANGUAGE_OPTIONS.values())
    return render_template('about-us.html', max_length=max_length)


@app.route('/blog')
def blog():
    max_length = max(len(option['name']) for option in LANGUAGE_OPTIONS.values())
    return render_template('blog.html', max_length=max_length)


@app.after_request
def add_header(response):
    # Extend caching to all static file types
    if (request.path.startswith('/static/') or
        request.path.endswith(('.webp', '.jpg', '.jpeg', '.png', '.css', '.js', '.mp4', '.webm'))):
        response.cache_control.max_age = 31536000  # 1 year
        response.cache_control.public = True
        # Add immutable for versioned files
        if 'v=' in request.path or '.min.' in request.path:
            response.cache_control.immutable = True
    return response


if __name__ == '__main__':
    app.run()
