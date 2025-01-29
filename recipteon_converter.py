import os
import json
import yaml
import shutil
from local_settings import *


def convert_time(text):
    text = text.lower()
    total_minutes = 0
    if "std" in text:
        hours = int(text.split("std")[0].strip())
        total_minutes += hours * 60
    if "min" in text:
        minutes = int(text.split("min")[0].split()[-1].strip())
        total_minutes += minutes
    return f"PT{total_minutes}M"


def json_to_yaml(json_file, yaml_file):
    with open(json_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # Konvertiere JSON in das gewünschte YAML-Format
    yaml_data = {
        "name": json_data["title"],
        "totalTime": convert_time(json_data.get("Gesamtzeit", "")),
        "prepTime": convert_time(json_data.get("Arbeitszeit", "")),
        "recipeYield": json_data.get("Portionen", ""),
        "recipeSections": [
            {
                "name": "Hauptzutaten",
                "ingredients": json_data["ingredients"],
                "instructions": json_data["steps"],
            }
        ],
        "nutrition": {
            "calories": json_data["nutritions"].get("brennwert"),
            "proteinContent": json_data["nutritions"].get("eiweiß"),
            "carbohydrateContent": json_data["nutritions"].get("kohlenhydrate"),
            "fatContent": json_data["nutritions"].get("fett"),
        },
        "keywords": json_data["tags"],
        "devices": [device.upper() for device in json_data["tm-versions"]],
        "locale": json_data["language"],
        "source": "cooki",
        "author": "Vorwerk",
        "difficulty": json_data["Schwierigkeitsgrad"],
    }

    # Optional: Versuche, den `hints`-Wert hinzuzufügen
    try:
        yaml_data["hints"] = json_data["hints"]
    except KeyError:
        pass

    with open(yaml_file, "w", encoding="utf-8") as f:
        yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)
    # print(f"Konvertiert: {json_file} -> {yaml_file}")


def process_recipes(outputdir):
    import_folder = "import-tmdata"
    recipes_folder = "recipes"
    image_folder = "images"
    for root, l_dirs, files in os.walk(outputdir):
        # Suche nach dem Unterordner "recipes"
        if recipes_folder in l_dirs:
            os.makedirs(os.path.join(root, import_folder), exist_ok=True)

        if recipes_folder in root:
            for file in files:
                if file.endswith(".json"):
                    json_path = os.path.join(root, file)
                    yaml_path = os.path.join(
                        root.replace(recipes_folder, import_folder),
                        file.replace(".json", ".yaml"),
                    )
                    json_to_yaml(json_path, yaml_path)
        if image_folder in root:
            for image in files:
                shutil.copy(
                    os.path.join(root, image),
                    os.path.join(root.replace(image_folder, import_folder), image),
                )


process_recipes(outputdir)
