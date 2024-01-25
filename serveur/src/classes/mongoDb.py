from pymongo import MongoClient
from pymongo.errors import PyMongoError

class MongoDBManager:
    """
    Classe pour gérer la connexion à une base de données MongoDB et fournir des références aux collections.
    Utilise le modèle de context manager pour une gestion efficace des ressources.
    """

    def __init__(self, uri, database_name):
        """
            Initialise une instance de MongoDBManager et établit une connexion à la base de données.

            :param uri: URI de connexion MongoDB incluant l'authentification et d'autres détails de connexion si nécessaire.
            :param database_name: Nom de la base de données à laquelle se connecter.
            
            Les collections existantes :
                -users
                
                -tickets
                
                -ticketsJ
                
                -badges
        """
        
        self.uri = uri
        self.database_name = database_name

        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.database_name]

            # Initialisation des collections
            self.users = self.db["users"]
            self.tickets = self.db["tickets"]
            self.ticketsJ = self.db["ticketsJ"]
            self.badges = self.db["badges"]
        except PyMongoError as e:
            print(f"Erreur lors de l'établissement de la connexion à MongoDB: {e}")
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()

    def get_collection(self, collection_name):
        """
            Récupère une référence à une collection dans la base de données.

            :param collection_name: Nom de la collection.
            :return: Référence à la collection.
        """
        return self.db[collection_name]

    def close(self):
        if self.client:
            self.client.close()