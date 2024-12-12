import requests
import pandas as pd
import sqlite3
import threading
from flask import Flask, render_template, request
import folium
from math import radians, sin, cos, sqrt, atan2
import time

# Fonction pour calculer la distance haversine
def haversine(lat1, lon1, lat2, lon2):
    """
    Calcule la distance entre deux points en kilomètres
    sur la surface de la Terre.
    """
    R = 6371  # Rayon moyen de la Terre en kilomètres
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


# Chemin vers la base de données SQLite
DB_PATH = "D:/Projets/API/data/info_velos.db"

# Initialiser l'application Flask
app = Flask(__name__)

# Fonction pour collecter les données depuis l'API de Paris
def collect_velib_data_paris():
    url_paris = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?"
    velib_data = []
    start = 0
    rows_per_page = 100
    while True:
        try:
            response = requests.get(url_paris, params={"start": start, "rows": rows_per_page})
            if response.status_code == 200:
                data = response.json()
                if "results" in data:
                    for record in data["results"]:
                        coordonnees_geo = record.get("coordonnees_geo", {})
                        velib_data.append({
                            "stationcode": record.get("stationcode"),
                            "name": record.get("name"),
                            "is_installed": record.get("is_installed"),
                            "capacity": record.get("capacity"),
                            "nombre_places_disponibles": record.get("numdocksavailable"),
                            "nombre_velos_disponibles": record.get("numbikesavailable"),
                            "longitude": coordonnees_geo.get("lon"),
                            "latitude": coordonnees_geo.get("lat"),
                            "arrondissement_commune": record.get("nom_arrondissement_communes"),
                            "code_insee_commune": record.get("code_insee_commune"),
                            "ville": "Paris"
                        })
                    start += rows_per_page
                    if len(data["results"]) < rows_per_page:
                        break
                else:
                    print("Erreur : clé 'results' non trouvée dans la réponse.")
                    break
            else:
                print(f"Erreur lors de la requête API : {response.status_code}")
                break
        except Exception as e:
            print(f"Erreur dans le décodage du JSON : {e}")
            break
    return velib_data

# Fonction pour collecter les données pour Toulouse
def collect_bike_data_toulouse():
    url_toulouse = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/stationnement-velo/records?limit=20"
    bike_data = []
    start = 0
    rows_per_page = 20
    while True:
        try:
            response = requests.get(url_toulouse, params={"start": start, "rows": rows_per_page})
            if response.status_code == 200:
                data = response.json()
                if "results" in data:
                    for record in data["results"]:
                        bike_data.append({
                            "arrondissement_commune": record.get("commune"),
                            "latitude": record["geo_point_2d"]["lat"],
                            "longitude": record["geo_point_2d"]["lon"],
                            "nombre_places_disponibles": record.get("nb_places"),
                            "nombre_velos_disponibles": record.get("nb_places") // 2,
                            "ville": "Toulouse"
                        })
                    start += rows_per_page
                    if len(data["results"]) < rows_per_page:
                        break
                else:
                    print("Erreur : clé 'results' non trouvée dans la réponse.")
                    break
            else:
                print(f"Erreur lors de la requête API : {response.status_code}")
                break
        except Exception as e:
            print(f"Erreur dans le décodage du JSON : {e}")
            break
    return bike_data

# Fonction pour collecter les données pour Lille
def collect_bike_data_lille():
    url_lille = "https://data.lillemetropole.fr/data/ogcapi/collections/vlille_temps_reel/items?"
    bike_data = []
    start = 0
    rows_per_page = 300
    while True:
        try:
            response = requests.get(url_lille, params={"start": start, "limit": rows_per_page}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "features" in data:
                    for record in data["features"]:
                        properties = record.get("properties", {})
                        geometry = record.get("geometry", {}).get("coordinates", [None, None])
                        bike_data.append({
                            "arrondissement_commune": properties.get("commune"),
                            "latitude": geometry[1],
                            "longitude": geometry[0],
                            "nombre_places_disponibles": properties.get("nb_places_dispo"),
                            "nombre_velos_disponibles": properties.get("nb_velos_dispo"),
                            "ville": "Lille"
                        })
                    start += rows_per_page
                    if len(data["features"]) < rows_per_page:
                        break
                else:
                    print("Erreur : clé 'features' non trouvée dans la réponse.")
                    break
            else:
                print(f"Erreur lors de la requête API : {response.status_code}")
                break
        except (requests.Timeout, requests.RequestException) as e:
            print(f"Erreur lors de la requête : {e}")
            break
    return bike_data

# Fonction pour stocker les données dans la base SQLite
def store_data_in_db(data):
    conn = sqlite3.connect(DB_PATH)
    df = pd.DataFrame(data)
    df.to_sql('clean_data', conn, if_exists='replace', index=False)
    conn.close()

# Fonction principale pour collecter et stocker les données
def collect_and_store_data():
    print("Collecte des données en cours...")
    paris_data = collect_velib_data_paris()
    toulouse_data = collect_bike_data_toulouse()
    lille_data = collect_bike_data_lille()
    all_data = paris_data + toulouse_data + lille_data
    store_data_in_db(all_data)
    print("Les données ont été collectées et stockées avec succès.")

# Thread pour actualiser les données toutes les 5 minutes
def data_updater():
    while True:
        collect_and_store_data()
        time.sleep(300)  # Pause de 5 minutes

# Initialiser le thread pour la collecte des données
thread = threading.Thread(target=data_updater, daemon=True)
thread.start()

# Flask: Fonction pour convertir une adresse en latitude et longitude
def geocode_address(adresse):
    api_key = "ce9ef8e9c3c84797baa3ba25164b1674"
    url = f"https://api.opencagedata.com/geocode/v1/json?q={adresse}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            latitude = data['results'][0]['geometry']['lat']
            longitude = data['results'][0]['geometry']['lng']
            return latitude, longitude
    return None, None

# Flask: Route pour afficher la page principale
@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT ville FROM clean_data")
    villes = [row[0] for row in cursor.fetchall()]
    conn.close()
    selected_ville = None
    map_html = None
    if request.method == "POST":
        selected_ville = request.form.get("ville")
        adresse = request.form.get("adresse")
        user_lat, user_lon = geocode_address(adresse)
        if user_lat and user_lon:
            map_html = generate_map(selected_ville, user_lat, user_lon)
    return render_template("map.html", villes=villes, map_html=map_html, selected_ville=selected_ville)

# Flask: Fonction pour générer une carte Folium
def generate_map(ville, user_lat, user_lon):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT arrondissement_commune, latitude, longitude, nombre_places_disponibles, nombre_velos_disponibles
        FROM clean_data WHERE ville = ?
    """, (ville,))
    stations = cursor.fetchall()
    conn.close()
    m = folium.Map(location=[user_lat, user_lon], zoom_start=15)
    folium.Marker(location=[user_lat, user_lon], popup="Votre position", icon=folium.Icon(color="red")).add_to(m)
    for station in stations:
        arrondissement, lat, lon, places, velos = station
        if haversine(user_lat, user_lon, lat, lon) <= 1:
            popup_info = f"Station : {arrondissement}<br>Places disponibles : {places}<br>Vélos disponibles : {velos}"
            folium.Marker(location=[lat, lon], popup=popup_info).add_to(m)
    return m._repr_html_()

# Lancer l'application Flask
if __name__ == "__main__":
    app.run(debug=True)
