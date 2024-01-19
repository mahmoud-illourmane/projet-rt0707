from app import db_manager
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from pymongo.errors import PyMongoError

class User:
    def __init__(self, db_manager, firstName, email, password, role, id=None):
        """
        Initialise un nouvel user ou charge un user existant.

        :param db_manager: Instance de MongoDBManager pour interagir avec la base de données.
        :param firstName: firstName de l'user.
        :param email: Email de l'user.
        :param password: Mot de passe de l'user (non hashé pour un nouveau, hashé pour un existant).
        :param role: Rôle de l'user.
        :param id: ID de l'user dans la base de données (pour un user existant).
        """
        
        self.db_manager = db_manager
        self.id = id
        self.firstName = firstName
        self.email = email
        self.password = password  # Doit être hashé si déjà existant.
        self.role = role
    
    def createUser(self):
        """
        Crée un nouvel user dans la base de données.
        """
        
        try:
            # Créez un document à insérer dans la collection
            user_data = {
                "firstName": "John",
                "email": "john@example.com",
                "password": "password123",
                "role": 1
            }

            result = self.db_manager.insert_one(user_data)
            self.id = result.inserted_id
            
            if result.inserted_id:
                # L'insertion a réussi, renvoyez une réponse de réussite
                response = {
                    'status': 201,
                    'id': str(result.inserted_id),
                    'first_name': user_data['firstName'],
                    'email': user_data['email']
                }
                print(response)
            else:
                # Gestion des erreurs si l'insertion a échoué
                print("L'insertion a échoué.")
        except PyMongoError as e:
            # Gestion des erreurs de PyMongo (par exemple, perte de connexion à la base de données)
            print(f"Une erreur PyMongo s'est produite : {str(e)}")
        except Exception as e:
            # Gestion d'autres exceptions non spécifiques à PyMongo
            print(f"Une erreur inattendue s'est produite : {str(e)}")
        finally:
            # Assurez-vous de fermer la connexion à la base de données, même en cas d'erreur
            self.db_manager.close_connection()
        
    def updateUser(self):
        """
        Met à jour un user existant dans la base de données.
        """
        if self.id:
            self.db_manager.get_users().update_one(
                {"_id": ObjectId(self.id)},
                {"$set": {
                    "firstName": self.firstName,
                    "email": self.email,
                    "password": self.password,  # Assurer que le mot de passe est déjà hashé.
                    "role": self.role
                }}
            )

    def deleteUser(self):
        """
        Supprime l'user de la base de données.
        """
        if self.id:
            self.db_manager.get_users().delete_one({"_id": ObjectId(self.id)})

    def to_json(self):
        """
        Retourne la représentation JSON de l'user.
        """
        return {
            "_id": str(self.id),
            "firstName": self.firstName,
            "email": self.email,
            "password": self.password,  # Le mot de passe doit être hashé.
            "role": self.role
        }

    @staticmethod
    def authUser(db_manager, email, password):
        """
        Charge un user existant à partir de la base de données en utilisant son ID.

        :param db_manager: Instance de MongoDBManager pour interagir avec la base de données.
        :param id_user: ID de l'user dans la base de données.
        :return: Une instance de user.
        """
        user_data = db_manager.get_users().find_one({"email": email, "password": password})
        if user_data:
            return User(
                db_manager,
                user_data["firstName"],
                user_data["email"],
                user_data["password"],
                user_data["role"],
                id=user_data["_id"]
            )
        return None
