import pygetwindow as gw

from core.registry import command


def _find(title_parts):
    if not title_parts:
        w = gw.getActiveWindow()
        if not w:
            raise RuntimeError("tidak ada jendela aktif")
        return w
    key = " ".join(title_parts).lower()
    for w in gw.getAllWindows():
        if w.title and key in w.title.lower():
            return w
    raise RuntimeError(f"jendela '{key}' tidak ditemukan (cek: jendela)")


@command("jendela", "windows", help="jendela  - daftar jendela yang terbuka")
def jendela(args):
    for w in gw.getAllWindows():
        if w.title.strip():
            print(f"  {w.title}")


@command("fokus", "focus", help="fokus <sebagian judul>  - pindah ke jendela itu")
def fokus(args):
    w = _find(args)
    if w.isMinimized:
        w.restore()
    try:
        w.activate()
    except Exception:  # trik klasik kalau Windows menolak activate
        w.minimize()
        w.restore()


@command("maksimal", "maximize", help="maksimal [judul]  - maksimalkan jendela")
def maksimal(args):
    _find(args).maximize()


@command("minimal", "minimize", help="minimal [judul]  - minimize jendela")
def minimal(args):
    _find(args).minimize()


@command("normal", "restore", help="normal [judul]  - kembalikan ukuran jendela")
def normal(args):
    _find(args).restore()


@command("tutupjendela", "closewin", help="tutupjendela [judul]  - tutup jendela dengan sopan (seperti klik X)")
def tutupjendela(args):
    _find(args).close()


@command("atur", "resize", help="atur <x> <y> <lebar> <tinggi> [judul]  - posisi & ukuran jendela")
def atur(args):
    if len(args) < 4:
        print("Pakai: atur x y lebar tinggi [judul]")
        return
    x, y, w_, h = map(int, args[:4])
    win = _find(args[4:])
    win.restore()
    win.moveTo(x, y)
    win.resizeTo(w_, h)
