from flask import Flask, render_template, redirect, url_for, session
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
    'en': {'name': 'English'}
}


def load_translations(lang_code):
    file_path = f"translations/{lang_code}.json"
    if not os.path.exists(file_path):
        file_path = "translations/pl.json"  # Default Language
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@app.route('/')
def index():
    if 'lang' not in session:
        session['lang'] = 'pl' # Default Language

    translations = load_translations(session['lang'])
    max_length = max(len(option['name']) for option in LANGUAGE_OPTIONS.values())
    return render_template('index.html',
                           translations=translations,
                           lang=session['lang'],
                           language_options=LANGUAGE_OPTIONS,
                           max_length=max_length)


@app.route('/<lang_code>')
def set_language(lang_code):
    if lang_code in LANGUAGE_OPTIONS:
        session['lang'] = lang_code

    logger.info(f"Language was set to {lang_code}")

    return redirect(url_for('index'))
