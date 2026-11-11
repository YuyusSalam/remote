from core.registry import COMMANDS, command


@command("bantuan", "help", "?", help="bantuan  - tampilkan semua perintah")
def bantuan(args):
    seen, groups = set(), {}
    for info in COMMANDS.values():
        if id(info) in seen:
            continue
        seen.add(id(info))
        groups.setdefault(info["module"], []).append(info)
    for mod, items in groups.items():
        print(f"\n[{mod}]")
        for i in items:
            print(f"  {i['help'] or i['name']}")
    print()
