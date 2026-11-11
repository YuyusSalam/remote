"""Parser + eksekutor baris perintah."""
import difflib
import re

from core import config
from core.registry import COMMANDS

MAX_DEPTH = 5


def tokenize(text):
    tokens = re.findall(r'"[^"]*"|\S+', text)
    return [t[1:-1] if len(t) >= 2 and t[0] == '"' and t[-1] == '"' else t for t in tokens]


def split_commands(line):
    """Pisahkan beberapa perintah dengan ';' (tanda ';' di dalam "kutip" aman)."""
    parts, buf, quoted = [], [], False
    for ch in line:
        if ch == '"':
            quoted = not quoted
        if ch == ";" and not quoted:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf))
    return [p.strip() for p in parts if p.strip()]


def run_one(text, depth=0):
    tokens = tokenize(text)
    if not tokens:
        return
    name, args = tokens[0].lower(), tokens[1:]

    info = COMMANDS.get(name)
    if info:
        try:
            info["fn"](args)
        except KeyboardInterrupt:
            print("[dibatalkan]")
        except Exception as e:  # satu perintah gagal tidak mematikan program
            print(f"[error] {type(e).__name__}: {e}")
        return

    macros = config.load("macros.json", {})
    if name in macros:
        if depth >= MAX_DEPTH:
            print("[error] macro terlalu dalam (rekursif?)")
            return
        run_line(macros[name], depth + 1)
        return

    guess = difflib.get_close_matches(name, list(COMMANDS) + list(macros), n=1)
    hint = f" Maksud kamu '{guess[0]}'?" if guess else ""
    print(f"Perintah '{name}' tidak dikenal.{hint} Ketik 'bantuan'.")


def run_line(line, depth=0):
    for part in split_commands(line):
        run_one(part, depth)
