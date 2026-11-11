import webbrowser
from urllib.parse import quote_plus

from core.registry import command


@command("cari", "google", help="cari <kata kunci>  - cari di Google")
def cari(args):
    webbrowser.open("https://www.google.com/search?q=" + quote_plus(" ".join(args)))


@command("yt", help="yt <kata kunci>  - cari di YouTube")
def yt(args):
    webbrowser.open("https://www.youtube.com/results?search_query=" + quote_plus(" ".join(args)))
