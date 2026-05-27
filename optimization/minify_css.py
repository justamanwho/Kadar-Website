import re
import os

# Znajdź główny folder projektu (ten z app.py)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Przejdź do parent folder (bo jesteś w optimization/)
project_dir = os.path.abspath(os.path.join(script_dir, '..'))

input_path = os.path.join(project_dir, 'static', 'styles.css')
output_path = os.path.join(project_dir, 'static', 'styles.min.css')
def safe_minify(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r';\s*', ';', css)
    css = re.sub(r':\s*', ':', css)
    css = re.sub(r'\s*{\s*', '{', css)
    css = re.sub(r'\s*}\s*', '}', css)
    css = re.sub(r',\s*', ',', css)
    return css.strip()


def minify_css(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            original = f.read()

        minified = safe_minify(original)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(minified)

        print("CSS minified!")

    except Exception as e:
        print(f"CSS error: {e}")


if __name__ == '__main__':
    minify_css(input_path, output_path)