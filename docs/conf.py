"""Configuration file for the Sphinx documentation builder."""

from typing import Any
from datetime import datetime

project = "First Athena Query"
year = datetime.now().year
copyright = f"{year} palewire"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "palewire"
pygments_style = "sphinx"

html_sidebars: dict[Any, Any] = {}
html_sidebars: dict[Any, Any] = {}
html_theme_options: dict[Any, Any] = {
    "canonical_url": "https://palewi.re/docs/first-athena-query/",
    "nosidebar": True,
}

extensions = [
    "myst_parser",
    "sphinx.ext.napoleon",
]
source_suffix = ".md"
master_doc = "index"