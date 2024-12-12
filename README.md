🚲 Stations de vélos en temps réel

![Capture d'écran 2024-12-09 202839](https://github.com/user-attachments/assets/9c1ffa64-0a8a-4740-b157-5fe26b362f1b)
![Capture d'écran 2024-12-09 203014](https://github.com/user-attachments/assets/b70be09f-e828-46b1-8551-073827bcdbdd)


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

📊 Visuals
Exemple de carte interactive
