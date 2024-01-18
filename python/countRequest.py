# -*- coding: utf-8 -*-

import json

# Charger le contenu du fichier .har
with open("localhostbis.har", "r", encoding="utf-8") as file:
    har_data = json.load(file)

# Initialiser le compteur
get_request_count = 0

# Parcourir toutes les entrées dans le fichier .har
for entry in har_data["log"]["entries"]:
    # Vérifier si la méthode de la requête est "GET"
    if entry["request"]["method"] == "GET" and entry["request"]["url"].startswith("https://tile.openstreetmap.org/"):
        get_request_count += 1

# Afficher le résultat
print("Nombre de requêtes pour chargement des tuiles :", get_request_count)