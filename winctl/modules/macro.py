from core import config
from core.registry import command


@command("macro", help='macro buat <nama> "<perintah ; perintah>" | jalan <nama> | daftar | hapus <nama>')
def macro(args):
    from core.dispatcher import run_line

    sub = args[0].lower() if args else "daftar"
    data = config.load("macros.json", {})

    if sub == "buat" and len(args) >= 3:
        data[args[1].lower()] = " ".join(args[2:])
        config.save("macros.json", data)
        print(f"Macro '{args[1]}' disimpan. Jalankan dengan: {args[1]}")
    elif sub == "jalan" and len(args) >= 2:
        if args[1].lower() not in data:
            print("Macro tidak ada.")
            return
        run_line(data[args[1].lower()])
    elif sub == "hapus" and len(args) >= 2:
        if data.pop(args[1].lower(), None) is not None:
            config.save("macros.json", data)
            print("Dihapus.")
    elif sub == "daftar":
        for k, v in data.items():
            print(f"  {k}: {v}")
        if not data:
            print("  (belum ada macro)")
    else:
        print('Pakai: macro buat <nama> "<perintah ; perintah>" | jalan <nama> | daftar | hapus <nama>')
