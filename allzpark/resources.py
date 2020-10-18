import os
from . import allzparkconfig
from .vendor.Qt import QtGui

dirname = os.path.dirname(__file__)
_cache = {}


def px(value, scale=1.0):
    return int(value * scale)


def find(*paths):
    fname = os.path.join(dirname, "resources", *paths)
    fname = os.path.normpath(fname)  # Conform slashes and backslashes
    return fname.replace("\\", "/")  # Cross-platform compatibility


def pixmap(*paths):
    path = find(*paths)
    basename = paths[-1]
    name, ext = os.path.splitext(basename)

    if not ext:
        path += ".png"

    try:
        pixmap = _cache[paths]
    except KeyError:
        pixmap = QtGui.QPixmap(find(*paths))
        _cache[paths] = pixmap

    return pixmap


def icon(*paths):
    return QtGui.QIcon(pixmap(*paths))


def load_style(palette_name, load_fonts=False):
    palettes = load_palettes()

    # Inject default resource path
    _res_root = os.path.join(dirname, "resources").replace("\\", "/")
    for p in palettes.values():
        p["res"] = _res_root

    with open(find("style.css")) as f:
        css = f.read() % palettes[palette_name]

    if load_fonts:
        _load_fonts()

    return css


def load_palettes():
    palettes = {
        "dark": {
            "brightest": "#403E3D",
            "bright": "#383635",
            "base": "#2E2C2C",
            "dim": "#21201F",
            "dimmest": "#141413",

            "highlight": "#69D6C2",
            "highlighted": "#111111",
            "active": "silver",
            "inactive": "dimGray",
        },

        "light": {
            "brightest": "#E9EAE6",
            "bright": "#DBDFDE",
            "base": "#D7D8D2",
            "dim": "#B3BABD",
            "dimmest": "#AEAEAF",

            "highlight": "#69D6C2",
            "highlighted": "#111111",
            "active": "black",
            "inactive": "darkSlateGray",
        },
    }
    if allzparkconfig.palettes:
        palettes.update(allzparkconfig.palettes)

    return palettes


def _load_fonts():
    """Load fonts from resources"""
    _res_root = os.path.join(dirname, "resources").replace("\\", "/")

    font_root = os.path.join(_res_root, "fonts")
    fonts = [
        "opensans/OpenSans-Bold.ttf",
        "opensans/OpenSans-BoldItalic.ttf",
        "opensans/OpenSans-ExtraBold.ttf",
        "opensans/OpenSans-ExtraBoldItalic.ttf",
        "opensans/OpenSans-Italic.ttf",
        "opensans/OpenSans-Light.ttf",
        "opensans/OpenSans-LightItalic.ttf",
        "opensans/OpenSans-Regular.ttf",
        "opensans/OpenSans-Semibold.ttf",
        "opensans/OpenSans-SemiboldItalic.ttf",

        "jetbrainsmono/JetBrainsMono-Bold.ttf"
        "jetbrainsmono/JetBrainsMono-Bold-Italic.ttf"
        "jetbrainsmono/JetBrainsMono-ExtraBold.ttf"
        "jetbrainsmono/JetBrainsMono-ExtraBold-Italic.ttf"
        "jetbrainsmono/JetBrainsMono-ExtraLight.ttf"
        "jetbrainsmono/JetBrainsMono-ExtraLight-Italic.ttf"
        "jetbrainsmono/JetBrainsMono-Italic.ttf"
        "jetbrainsmono/JetBrainsMono-Light.ttf"
        "jetbrainsmono/JetBrainsMono-Light-Italic.ttf"
        "jetbrainsmono/JetBrainsMono-Medium.ttf"
        "jetbrainsmono/JetBrainsMono-Medium-Italic.ttf"
        "jetbrainsmono/JetBrainsMono-Regular.ttf"
        "jetbrainsmono/JetBrainsMono-SemiLight.ttf"
        "jetbrainsmono/JetBrainsMono-SemiLight-Italic.ttf"
    ]

    for font in fonts:
        path = os.path.join(font_root, font)
        QtGui.QFontDatabase.addApplicationFont(path)
