"""Registry perintah. Modul cukup pakai @command(...) untuk mendaftarkan perintah."""

COMMANDS = {}


def command(name, *aliases, help=""):
    def deco(fn):
        info = {
            "fn": fn,
            "name": name,
            "help": help,
            "module": fn.__module__.split(".")[-1],
        }
        for n in (name, *aliases):
            COMMANDS[n.lower()] = info
        return fn

    return deco
