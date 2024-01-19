from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

class MongoDBManager:
    """
        Classe pour gérer la connexion à une base de données MongoDB et fournir des références aux collections.
    """

    def __init__(self, host, port, database_name):
        """
            Initialise une instance de MongoDBManager et établit une connexion à la base de données.

            :param host: Adresse IP ou nom d'hôte du serveur MongoDB.
            :param port: Port du serveur MongoDB (par exemple, 27017 par défaut).
            :param database_name: Nom de la base de données à laquelle se connecter.
        """
        
        try:
            self.client = MongoClient(host, port)
        except ConnectionFailure as e:
            print(f"Erreur de connexion à MongoDB: {e}")
            raise
        except PyMongoError as e:
            print(f"Erreur PyMongo: {e}")
            raise

        self.db = self.client[database_name]
        self.users = self.db["users"]
        self.tickets = self.db["tickets"]
        self.ticketsJ = self.db["ticketsJ"]
        self.badges = self.db["badges"]

    def get_users(self):
        """
        Récupère une référence à la collection "users" dans la base de données.
        :return: Référence à la collection "users".
        """
        return self.users

    def get_tickets(self):
        """
        Récupère une référence à la collection "tickets" dans la base de données.
        :return: Référence à la collection "tickets".
        """
        return self.tickets
    
    def get_tickets_j(self):
        """
        Récupère une référence à la collection "ticketsJ" dans la base de données.
        :return: Référence à la collection "ticketsJ".
        """
        return self.ticketsJ

    def get_badges(self):
        """
        Récupère une référence à la collection "badges" dans la base de données.
        :return: Référence à la collection "badges".
        """
        return self.badges

    def close_connection(self):
        """
        Ferme proprement la connexion à la base de données MongoDB.
        """
        try:
            self.client.close()
        except PyMongoError as e:
            print(f"Erreur lors de la fermeture de la connexion MongoDB: {e}")
            raise
