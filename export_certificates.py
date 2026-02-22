#!/usr/bin/python3
import json
import base64
from pathlib import Path
import os

# Konfigurierbare Pfade
ACME_JSON_PATH = "acme.json"
OUTPUT_DIR = "output"
DOMAIN_NAME = "iobroker.limhu.duckdns.org"  # Ersetze mit deiner tatsächlichen Domain

# Sicherstellen, dass das Zielverzeichnis existiert
Path(os.path.join(OUTPUT_DIR, DOMAIN_NAME)).mkdir(parents=True, exist_ok=True)

# acme.json laden
with open(ACME_JSON_PATH, "r") as f:
    data = json.load(f)

# data = data["myresolver"]
# Zertifikate suchen
for entry in data.get("myresolver", {}).get("Certificates", []):
    if entry["domain"]["main"] == DOMAIN_NAME:
        cert_data = base64.b64decode(entry["certificate"])
        key_data = base64.b64decode(entry["key"])

        # Zertifikate speichern
        cert_path = Path(OUTPUT_DIR) / "fullchain.pem"
        key_path = Path(OUTPUT_DIR) / "privkey.pem"

        with open(cert_path, "wb") as cert_file:
            cert_file.write(cert_data)

        with open(key_path, "wb") as key_file:
            key_file.write(key_data)

        print(f"Zertifikate für {DOMAIN_NAME} gespeichert:")
        print(f"- Zertifikat: {cert_path}")
        print(f"- Private Key: {key_path}")
        break
else:
    print(f"Kein Zertifikat für {DOMAIN_NAME} gefunden!")
