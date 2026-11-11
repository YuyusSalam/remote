import time

import pyautogui

from core.registry import command

pyautogui.FAILSAFE = True  # gerakkan mouse ke pojok kiri-atas layar = STOP darurat
pyautogui.PAUSE = 0.05


def _paste(text):
    """Untuk teks non-ASCII (emoji, aksara lain): lewat clipboard."""
    import tkinter as tk

    r = tk.Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.update()
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.2)
    r.destroy()


@command("ketik", "type", help="ketik <teks>  - ketik di jendela aktif (pakai 'fokus' dulu)")
def ketik(args):
    text = " ".join(args)
    if text.isascii():
        pyautogui.write(text, interval=0.01)
    else:
        _paste(text)


@command("tekan", "press", help="tekan <tombol>  - contoh: tekan enter | tekan ctrl+c | tekan win+d")
def tekan(args):
    if not args:
        print("Pakai: tekan <tombol> (gabungan pakai +)")
        return
    keys = [k.strip().lower() for k in args[0].split("+")]
    keys = ["win" if k in ("windows", "super") else k for k in keys]
    if len(keys) == 1:
        pyautogui.press(keys[0])
    else:
        pyautogui.hotkey(*keys)


@command("klik", "click", help="klik [kiri|kanan|dobel] [x y]  - klik di posisi (atau posisi mouse saat ini)")
def klik(args):
    mode, nums = "kiri", []
    for a in args:
        if a.lstrip("-").isdigit():
            nums.append(int(a))
        else:
            mode = a.lower()
    kw = {"x": nums[0], "y": nums[1]} if len(nums) >= 2 else {}
    if mode in ("kanan", "right"):
        pyautogui.rightClick(**kw)
    elif mode in ("dobel", "double"):
        pyautogui.doubleClick(**kw)
    else:
        pyautogui.click(**kw)


@command("pindah", "move", help="pindah <x> <y>  - gerakkan mouse")
def pindah(args):
    pyautogui.moveTo(int(args[0]), int(args[1]), duration=0.2)


@command("gulir", "scroll", help="gulir <n>  - scroll (positif=atas, negatif=bawah)")
def gulir(args):
    pyautogui.scroll(int(args[0]) * 100)


@command("posisi", "pos", help="posisi  - tampilkan posisi mouse & ukuran layar")
def posisi(args):
    print(f"Mouse: {tuple(pyautogui.position())}  Layar: {tuple(pyautogui.size())}")
