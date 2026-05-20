from flask import Flask, render_template_string, redirect, url_for, session, request, g, make_response
from dotenv import load_dotenv
from main_routes import bp
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

# @app.before_request
# def log_request_info():
#     print(f"📡 Request: {request.method} {request.path}")
#
# @app.route('/sitemap.xml')
# def sitemap_xml():
#     print("🔥🔥🔥 JESTEM W FUNKCJI SITEMAP! 🔥🔥🔥")
#     base_url = 'https://kadarprzeprowadzki.pl'
#
#     # Lista nazw Twoich stron (bez języka)
#     slugs = ['o-nas', 'kontakt', 'blog', 'credits']
#     blog_posts = ['naczynia', 'zwierzeta', 'bezwindy', 'bielsko']
#     languages = ['pl', 'en', 'de', 'ukr']
#
#     pages = []
#
#     for lang in languages:
#         # Główne strony
#         for slug in slugs:
#             if slug == '':
#                 url = f'{base_url}/{lang}/'
#                 priority = '0.9' if lang == 'pl' else '0.8'
#             else:
#                 url = f'{base_url}/{lang}/{slug}'
#                 priority = '0.7' if lang == 'pl' else '0.6'
#             pages.append({'loc': url, 'priority': priority})
#
#         # Wpisy blogowe
#         for post in blog_posts:
#             url = f'{base_url}/{lang}/blog/{post}'
#             priority = '0.6'
#             pages.append({'loc': url, 'priority': priority})
#
#     # Dodajesz tutaj wszystkie wersje językowe
#     lang_codes = ['pl', 'en', 'de', 'ukr']
#     for code in lang_codes:
#         pages.append({'loc': f'{base_url}/{code}/', 'priority': '0.9'})
#         pages.append({'loc': f'{base_url}/{code}/blog', 'priority': '0.8'})
#         # ... analogicznie dla innych podstron
#
#     # Tworzysz XML
#     sitemap_xml = render_template_string('''
# <?xml version="1.0" encoding="UTF-8"?>
# <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
#     {% for page in pages %}
#     <url>
#         <loc>{{ page.loc }}</loc>
#         <priority>{{ page.priority }}</priority>
#     </url>
#     {% endfor %}
# </urlset>
# ''', pages=pages)
#
#     response = make_response(sitemap_xml)
#     response.headers['Content-Type'] = 'application/xml'
#     return response


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
    # Always default to Polish, ignoring browser language
    session['lang'] = 'pl'
    return redirect(url_for('main.index', lang_code='pl'))


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