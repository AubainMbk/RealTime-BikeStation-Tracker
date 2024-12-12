 # Stations de vélos en temps réel

![Capture d'écran 2024-12-09 20289](https://github.com/user-attachments/assets/b0a66d2b-49a9-4b28-859c-be16decfc118)



Visualisez et suivez les stations de vélos en temps réel avec une interface intuitive et interactive.

🌟 À propos

BikeStationMap est une application web innovante qui permet aux utilisateurs :

    🌍 D’afficher les stations de vélos disponibles à Paris, Lille et Toulouse.
    📍 De rechercher les stations proches d’une adresse saisie grâce à un système de géocodage.
    📊 De visualiser en temps réel le nombre de places et de vélos disponibles.

L'application est conçue pour être rapide, pratique, et adaptée à une gestion de données en temps réel.
📋 Fonctionnalités

    Interface interactive : Une carte intuitive centrée sur l’utilisateur.
    Recherche par adresse : Conversion des adresses en coordonnées géographiques grâce à un géocodage précis.
    Filtrage avancé : Affiche uniquement les stations dans un rayon de 1 km autour de l’utilisateur.
    Données en temps réel : Mise à jour automatique des stations toutes les deux minutes.
    Support multi-villes : Paris, Lille et Toulouse.

📂 Structure du projet

    /data : Contient la base de données SQLite pour stocker les informations des stations.
    /templates : Fichiers HTML pour l'interface utilisateur Flask.
    /static : Images et styles CSS pour l’application web.
    app.py : Code principal Flask pour l'application web.
    collect_data.py : Script de collecte et de stockage des données en temps réel.

🛠️ Technologies utilisées

    Langage : Python
    Framework : Flask
    Base de données : SQLite
    Visualisation : Folium
    API : OpenCage Geocoder pour le géocodage des adresses
    Planification : APScheduler

📊 Visuels
Exemples
![Capture d'écran 2024-12-12 215135](https://github.com/user-attachments/assets/fbdfed13-a78f-447a-bbf2-aa10ab69af74)
![Capture d'écran 2024-12-12 215228](https://github.com/user-attachments/assets/0fb173b1-60d5-40bf-a6b8-1f9abf29251f)
![Capture d'écran 2024-12-12 215625](https://github.com/user-attachments/assets/96fa6b0f-19c4-4175-9909-9db591118456)


