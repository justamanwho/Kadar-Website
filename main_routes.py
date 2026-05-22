from flask import Blueprint, render_template, session, current_app, g
import os
import json

bp = Blueprint('main', __name__, url_prefix='/<lang_code>')

LANGUAGE_OPTIONS = {
    'pl': {'name': 'Polski'},
    'en': {'name': 'English'},
    'de': {'name': 'Deutsch'},
    'ukr': {'name': 'Українська'},
    'ja': {'name': '日本語'}
}


def load_translations(lang_code):
    """Load translations for a given language"""
    file_path = f"translations/{lang_code}.json"
    if not os.path.exists(file_path):
        file_path = "translations/pl.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    """Extract language code from URL and store it in g"""
    if values:
        g.lang_code = values.pop('lang_code')
    else:
        g.lang_code = session.get('lang', 'pl')

    g.translations = load_translations(g.lang_code)
    g.language_options = LANGUAGE_OPTIONS


@bp.url_defaults
def add_lang_code(endpoint, values):
    """Automatically add language code to all url_for() calls"""
    if 'lang_code' in values or not g.get('lang_code'):
        return
    if current_app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
        values['lang_code'] = g.lang_code


# ============== ROUTES ==============

@bp.route('/')
def index():
    gallery_path = os.path.join(current_app.static_folder, "gallery")
    files = sorted(os.listdir(gallery_path))

    gallery_files = []
    for f in files:
        if '_compressed' in f or f.lower().endswith('webp'):
            continue
        ext = f.lower().split('.')[-1]
        if ext in ['jpg', 'jpeg', 'png', 'mp4', 'mov', 'webm']:
            gallery_files.append({
                "name": f,
                "is_video": ext in ["mp4", "mov", "webm"]
            })

    max_length = max(len(option['name']) for option in LANGUAGE_OPTIONS.values())

    return render_template('index.html',
                           max_length=max_length,
                           gallery_files=gallery_files)


@bp.route('/kontakt')
def contact():
    max_length = max(len(option['name']) for option in LANGUAGE_OPTIONS.values())
    return render_template('contact.html', max_length=max_length)


@bp.route('/o-nas')
def about():
    max_length = max(len(option['name']) for option in LANGUAGE_OPTIONS.values())
    return render_template('about-us.html', max_length=max_length)


@bp.route('/blog')
def blog():
    max_length = max(len(option['name']) for option in LANGUAGE_OPTIONS.values())
    return render_template('blog.html', max_length=max_length)

# 1
@bp.route('/blog/poradnik')
def blog_poradnik():
    return render_template('blog_poradnik.html')


# 2
@bp.route('/blog/naczynia')
def blog_naczynia():
    return render_template('blog_naczynia.html')

# 3
@bp.route('/blog/zwierzeta')
def blog_zwierzeta():
    return render_template('blog_zwierzeta.html')

# 4
@bp.route('/blog/bezwindy')
def blog_bezwindy():
    return render_template('blog_bezwindy.html')

# 5
@bp.route('/blog/bielsko')
def blog_bielsko():
    return render_template('blog_bielsko.html')

# 6
@bp.route('/blog/pianino')
def blog_pianino():
    return render_template('blog_pianino.html')

# 7
@bp.route('/blog/ukryte-koszty')
def blog_ukryte_koszty():
    return render_template('blog_ukryte_koszty.html')

# 8
@bp.route('/blog/wycena')
def blog_wycena():
    return render_template('blog_wycena.html')

# 9
@bp.route('/blog/biuro')
def blog_biuro():
    return render_template('blog_biuro.html')

# 10
@bp.route('/blog/magazyn')
def blog_magazyn():
    return render_template('blog_magazyn.html')

# 11
@bp.route('/blog/sejf')
def blog_sejf():
    return render_template('blog_sejf.html')

# 12
@bp.route('/blog/kartony')
def blog_kartony():
    return render_template('blog_kartony.html')

# 13
@bp.route('/blog/walizka')
def blog_walizka():
    return render_template('blog_walizka.html')

# 14
@bp.route('/blog/lato')
def blog_lato():
    return render_template('blog_lato.html')

# 15
@bp.route('/blog/zima')
def blog_zima():
    return render_template('blog_zima.html')

# 16
@bp.route('/blog/weekend')
def blog_weekend():
    return render_template('blog_weekend.html')

# 17
@bp.route('/blog/wybor-firmy')
def blog_wybor_firmy():
    return render_template('blog_wybor_firmy.html')

# 18
@bp.route('/blog/antyki')
def blog_antyki():
    return render_template('blog_antyki.html')

# 19
@bp.route('/blog/list')
def blog_list():
    return render_template('blog_list.html')

# 20
@bp.route('/blog/dzieci')
def blog_dzieci():
    return render_template('blog_dzieci.html')


@bp.route('/credits')
def credits():
    max_length = max(len(option['name']) for option in LANGUAGE_OPTIONS.values())
    return render_template('credits.html', max_length=max_length)
