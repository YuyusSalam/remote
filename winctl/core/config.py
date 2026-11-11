"""Baca/tulis file JSON di folder program (apps.json, macros.json)."""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_APPS = {
    "kalkulator": "calc",
    "catatan": "notepad",
    "notepad": "notepad",
    "paint": "mspaint",
    "cmd": "cmd",
    "powershell": "powershell",
    "explorer": "explorer",
    "file": "explorer",
    "pengaturan": "ms-settings:",
    "taskmanager": "taskmgr",
    "chrome": "chrome",
    "edge": "msedge",
    "firefox": "firefox",
    "word": "winword",
    "excel": "excel",
    "vscode": "code",
}


def path(*parts):
    return os.path.join(BASE, *parts)


def load(name, default):
    try:
        with open(path(name), encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save(name, data):
    with open(path(name), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def apps():
    """Alias aplikasi = bawaan + isi apps.json milik user."""
    merged = dict(DEFAULT_APPS)
    merged.update({k.lower(): v for k, v in load("apps.json", {}).items()})
    return merged
