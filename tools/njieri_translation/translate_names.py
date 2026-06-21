import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

POKEMON_FILES = [
    ROOT / "src/data/pokemon/species_info/gen_1_families.h",
    ROOT / "src/data/pokemon/species_info/gen_2_families.h",
    ROOT / "src/data/pokemon/species_info/gen_3_families.h",
    ROOT / "src/data/pokemon/species_info/gen_4_families.h",
    ROOT / "src/data/pokemon/species_info/gen_5_families.h",
]

MOVES_FILE = ROOT / "src/data/moves_info.h"

UI_FILES = [
    ROOT / "src/strings.c",
    ROOT / "src/main_menu.c",
    ROOT / "src/option_menu.c",
    ROOT / "src/data/party_menu.h",
    ROOT / "src/data/trade.h",
    ROOT / "src/pokemon_storage_system.c",
    ROOT / "src/pokenav_match_call_gfx.c",
    ROOT / "src/data/easy_chat/easy_chat_group_trainer.h",
    ROOT / "src/data/easy_chat/easy_chat_group_trendy_saying.h",
]

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def replace_in_file(path, replacements, mode):
    if not path.exists():
        print(f"Missing: {path.relative_to(ROOT)}")
        return

    text = path.read_text(encoding="utf-8")
    old_text = text

    for english, german in replacements.items():
        if mode == "pokemon":
            text = text.replace(
                f'.speciesName = _("{english}")',
                f'.speciesName = _("{german}")'
            )

        elif mode == "moves":
            text = text.replace(
                f'.name = COMPOUND_STRING("{english}")',
                f'.name = COMPOUND_STRING("{german}")'
            )

        elif mode == "ui":
            text = text.replace(f'_("{english}")', f'_("{german}")')
            text = text.replace(f'COMPOUND_STRING("{english}")', f'COMPOUND_STRING("{german}")')

    if text != old_text:
        path.write_text(text, encoding="utf-8")
        print(f"Updated: {path.relative_to(ROOT)}")
    else:
        print(f"No changes: {path.relative_to(ROOT)}")

def main():
    pokemon = load_json(ROOT / "tools/njieri_translation/pokemon_de.json")
    moves = load_json(ROOT / "tools/njieri_translation/moves_de.json")
    ui = load_json(ROOT / "tools/njieri_translation/ui_de.json")

    for file in POKEMON_FILES:
        replace_in_file(file, pokemon, "pokemon")

    replace_in_file(MOVES_FILE, moves, "moves")

    for file in UI_FILES:
        replace_in_file(file, ui, "ui")

if __name__ == "__main__":
    main()