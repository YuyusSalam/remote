"""WinCtl - kontrol Windows lewat perintah teks.

  python run.py                 -> mode interaktif (REPL)
  python run.py buka notepad    -> jalankan satu baris lalu keluar
"""
import importlib
import pkgutil
import sys


def _dpi_aware():
    try:
        import ctypes

        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # koordinat klik akurat di layar scaling
    except Exception:
        pass


def load_modules():
    """Auto-load semua file di folder modules/. Modul yang dependensinya kurang dilewati."""
    import modules

    for m in pkgutil.iter_modules(modules.__path__):
        try:
            importlib.import_module(f"modules.{m.name}")
        except ImportError as e:
            print(f"[lewati] modul '{m.name}' belum bisa dipakai: {e}")


def main():
    if sys.platform != "win32":
        print("[peringatan] program ini dibuat untuk Windows; sebagian perintah tidak akan jalan.")
    _dpi_aware()
    load_modules()
    from core.dispatcher import run_line

    if len(sys.argv) > 1:
        line = " ".join(f'"{a}"' if " " in a else a for a in sys.argv[1:])
        run_line(line)
        return

    print("WinCtl siap. 'bantuan' = daftar perintah, 'keluar' = berhenti.")
    print("Gabung perintah dengan ';'  contoh: buka notepad ; tunggu 1 ; ketik halo")
    while True:
        try:
            line = input("win> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line.lower() in ("keluar", "exit", "quit"):
            break
        run_line(line)


if __name__ == "__main__":
    main()
