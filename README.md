# StreamerAPI

---
Demo twitch streamers project implemented with flask-restful and postgresql

## How to install

1. clone the project
2. Navigate to the folder (cd inside the folder)
3. create a .env according to the .env.example file containing your twitch client-id and client-secret


## How to run

1. install docker to your local computer if it's not already installed
2. navigate to the folder
3. run `docker-compose up` or `docker-compose up -d` if you want to run the project in detach mode.


## Principaux Urls de l'api
 - GET localhost:5000/streamers :  Obtenir la liste des streamers
 - POST localhost :5000/streamers/{username} : Ajouter un streamer à la base de données
 - DELETE localhost :5000/streamers/{username} : Suppression d'un streamer de la base de données