import sys
import os
from sphinx.builders.html import StandaloneHTMLBuilder

sys.path.append(os.path.abspath('..'))
# Kindda hack the import to import shared config file
sys.path.append(os.path.abspath('.'))
from front_end.config import shared_conf
from front_end.config import base_conf

# -- Project information -----------------------------------------------------

project = u'PyNiryo2'
copyright = shared_conf.copyright
author = shared_conf.author

# The short X.Y version
version = u'v1.0'
# The full version, including alpha/beta/rc tags
release = u'v1.0.0'

# -- General configuration ---------------------------------------------------

extensions = base_conf.extensions

StandaloneHTMLBuilder.supported_image_types = [
    'image/svg+xml',
    'image/gif',
    'image/png',
    'image/jpeg'
]

# Avoid autosection label to trigger warning on low level titles
autosectionlabel_maxdepth = 3
# Avoid clash between same label in different document
autosectionlabel_prefix_document = True
autoclass_content = 'both'

# Todo_extension
todo_include_todos = True
todo_emit_warnings = True

# Documentation infos
source_suffix = '.rst'
master_doc = 'index'

for arg in sys.argv:
    if not arg.startswith("language="):
        continue
    else:
        language = arg.replace("language=", "")
        break
else:
    language = None

translation_object = {}
translation_object["fr"] = {}
translation_object["fr"]["PROJECT_NAME"] = "PyNiryo2"

translation_object["en"] = {}
translation_object["en"]["PROJECT_NAME"] = "PyNiryo2"

html_context = {}

html_context["BASE_FOLDER_URL"] = "https://docs.niryo.com/dev/pyniryo2"


html_context["TRANSLATION"] = translation_object[language if language is not None else 'en']

exclude_patterns = [u'_build', 'Thumbs.db', '.DS_Store']

pygments_style = None

add_module_names = False


# -- Options for HTML output -------------------------------------------------
html_theme = shared_conf.html_theme

templates_path = shared_conf.templates_path
html_static_path = shared_conf.html_static_path

html_logo = shared_conf.html_logo
html_favicon = shared_conf.html_favicon

html_css_files = shared_conf.html_css_files

html_js_files = shared_conf.html_js_files

html_theme_options = shared_conf.html_theme_options

html_show_sphinx = shared_conf.html_show_sphinx

# -- Options for intersphinx extension ---------------------------------------

# Links
extlinks = {
}

# -- Internationalization --
locale_dirs = ['locale/']  # path is example but recommended.
gettext_compact = False  # optional.

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'https://docs.python.org/': None,
}

# Toggle button text
togglebutton_hint = ""