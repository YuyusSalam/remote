import os
import subprocess

from core import config
from core.registry import command


def launch(target):
    aliases = config.apps()
    if target.lower() in aliases:
        target = aliases[target.lower()]
    else:
        first, _, rest = target.partition(" ")
        if rest and first.lower() in aliases:
            target = f"{aliases[first.lower()]} {rest}"
    try:
        os.startfile(target)  # app, file, folder, URL, ms-settings:
    except OSError:
        subprocess.Popen(f'start "" {target}', shell=True)


@command("buka", "open", help='buka <app|file|folder|url> [argumen]  - contoh: buka chrome https://google.com')
def buka(args):
    if not args:
        print("Pakai: buka <app|file|folder|url>")
        return
    launch(" ".join(args))


@command("tutup", "kill", help="tutup <nama proses>  - hentikan proses, contoh: tutup chrome")
def tutup(args):
    import psutil

    name = " ".join(args).lower().removesuffix(".exe")
    if len(name) < 3:
        print("Nama proses minimal 3 huruf.")
        return
    count = 0
    for p in psutil.process_iter(["name"]):
        pname = (p.info["name"] or "").lower().removesuffix(".exe")
        if pname.startswith(name):
            try:
                p.terminate()
                count += 1
            except psutil.Error:
                pass
    print(f"{count} proses dihentikan.")


@command("proses", "ps", help="proses [filter]  - daftar proses (urut pemakaian RAM)")
def proses(args):
    import psutil

    flt = " ".join(args).lower()
    rows = []
    for p in psutil.process_iter(["pid", "name", "memory_info"]):
        n = p.info["name"] or ""
        if flt in n.lower() and p.info["memory_info"]:
            rows.append((p.info["memory_info"].rss / 1e6, p.info["pid"], n))
    for mb, pid, n in sorted(rows, reverse=True)[:25]:
        print(f"{pid:>7}  {mb:8.1f} MB  {n}")


@command("alias", help="alias <nama> <target>  - simpan singkatan aplikasi ke apps.json")
def alias(args):
    if len(args) < 2:
        print("Pakai: alias <nama> <path/perintah>")
        return
    data = config.load("apps.json", {})
    data[args[0].lower()] = " ".join(args[1:])
    config.save("apps.json", data)
    print(f"Alias '{args[0]}' disimpan.")
