import ctypes
import datetime
import os
import subprocess
import time

from core import config
from core.registry import command


def _confirm(msg):
    return input(f"{msg} (y/n): ").strip().lower() in ("y", "ya")


@command("tunggu", "wait", help="tunggu <detik>  - jeda antar perintah")
def tunggu(args):
    time.sleep(float(args[0]))


@command("bersih", "cls", help="bersih  - bersihkan layar terminal")
def bersih(args):
    os.system("cls")


@command("volume", help="volume naik|turun|mute [langkah]  - atur volume sistem")
def volume(args):
    import pyautogui

    act = args[0].lower() if args else ""
    n = int(args[1]) if len(args) > 1 else 5
    key = {"naik": "volumeup", "up": "volumeup", "turun": "volumedown",
           "down": "volumedown", "mute": "volumemute", "bisu": "volumemute"}.get(act)
    if not key:
        print("Pakai: volume naik|turun|mute [langkah]")
        return
    pyautogui.press(key, presses=1 if key == "volumemute" else n)


@command("kunci", "lock", help="kunci  - kunci layar Windows")
def kunci(args):
    ctypes.windll.user32.LockWorkStation()


@command("screenshot", "ss", help="screenshot [nama]  - simpan tangkapan layar ke folder screenshots/")
def screenshot(args):
    import pyautogui

    os.makedirs(config.path("screenshots"), exist_ok=True)
    name = args[0] if args else datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    p = config.path("screenshots", f"{name}.png")
    pyautogui.screenshot(p)
    print(f"Tersimpan: {p}")


@command("info", help="info  - CPU, RAM, baterai")
def info(args):
    import psutil

    print(f"CPU : {psutil.cpu_percent(interval=0.5)}%")
    print(f"RAM : {psutil.virtual_memory().percent}%")
    b = psutil.sensors_battery()
    if b:
        print(f"Baterai: {b.percent}% ({'dicas' if b.power_plugged else 'baterai'})")


@command("jalankan", "sh", help="jalankan <perintah cmd>  - eksekusi perintah CMD, contoh: jalankan ipconfig")
def jalankan(args):
    subprocess.run(" ".join(args), shell=True)


@command("pwsh", help="pwsh <perintah>  - eksekusi perintah PowerShell")
def pwsh(args):
    subprocess.run(["powershell", "-NoProfile", "-Command", " ".join(args)])


@command("matikan", "shutdown", help="matikan  - shutdown PC dalam 15 detik (minta konfirmasi)")
def matikan(args):
    if _confirm("Matikan komputer?"):
        subprocess.run("shutdown /s /t 15", shell=True)
        print("Ketik 'batalmatikan' untuk membatalkan.")


@command("restart", help="restart  - restart PC dalam 15 detik (minta konfirmasi)")
def restart(args):
    if _confirm("Restart komputer?"):
        subprocess.run("shutdown /r /t 15", shell=True)
        print("Ketik 'batalmatikan' untuk membatalkan.")


@command("batalmatikan", help="batalmatikan  - batalkan shutdown/restart yang tertunda")
def batalmatikan(args):
    subprocess.run("shutdown /a", shell=True)
