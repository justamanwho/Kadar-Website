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


@app.before_request
def redirect_without_language():
    path = request.path
    if path.startswith('/static/') or path == '/sitemap-main.xml':
        return
    if not path.startswith(('/pl/', '/en/', '/de/', '/ukr/', '/ja/')):
        return redirect(f'/pl{path}', code=301)


@app.route('/sitemap-main.xml')
def sitemap_xml():
    base_url = 'https://kadarprzeprowadzki.pl'

    blog_posts = ['poradnik', 'naczynia', 'zwierzeta', 'bezwindy', 'bielsko',
                  'pianino', 'ukryte-koszty', 'wycena', 'biuro', 'magazyn',
                  'sejf', 'kartony', 'walizka', 'lato', 'zima', 'weekend',
                  'wybor-firmy', 'antyki', 'list', 'dzieci']

    # Główne strony
    slugs = ['', 'o-nas', 'kontakt', 'blog', 'credits']
    languages = ['pl', 'en', 'de', 'ukr']

    pages = []

    for lang in languages:
        for slug in slugs:
            if slug == '':
                url = f'{base_url}/{lang}/'
                priority = '1.0' if lang == 'pl' else '0.9'
            else:
                url = f'{base_url}/{lang}/{slug}'
                priority = '0.8' if lang == 'pl' else '0.7'
            pages.append({'loc': url, 'priority': priority})

        for post in blog_posts:
            url = f'{base_url}/{lang}/blog/{post}'
            priority = '0.7'
            pages.append({'loc': url, 'priority': priority})

    unique_pages = []
    seen_urls = set()
    for page in pages:
        if page['loc'] not in seen_urls:
            seen_urls.add(page['loc'])
            unique_pages.append(page)

    # Generuj XML
    sitemap_xml = render_template_string('''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {% for page in pages %}
    <url>
        <loc>{{ page.loc }}</loc>
        <priority>{{ page.priority }}</priority>
    </url>
    {% endfor %}
</urlset>''', pages=unique_pages)

    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response


app.register_blueprint(bp)

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