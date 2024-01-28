from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from pymongo.errors import PyMongoError
import datetime, re

from src.classes.mongoDb import MongoDBManager
from src.classes.qrCode import QRCode

class User:
    def __init__(self, db_manager: MongoDBManager, firstName, email, password, role, id=None):
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
        self.password = password
        self.role = role
    
    def createUser(self):
        """
            Crée un nouvel utilisateur dans la base de données.
        """
        
        try:
            # Vérification de si l'email existe déjà
            users_collection = self.db_manager.get_collection('users')
            if users_collection.find_one({'email': self.email}):
                return jsonify({
                    'status': 400,
                    'error': 'Email déjà utilisé'
                }), 400

            if self.role not in [1, 2, 3]:
                return jsonify({
                    'status': 400,
                    'error': 'La valeur du rôle n\'est pas reconnue.'
                }), 400

            # Hacher le mot de passe avant de l'insérer
            hashed_password = generate_password_hash(self.password)

            # Créer le document utilisateur
            user_data = {
                'firstName': self.firstName,
                'email': self.email,
                'password': hashed_password,
                'role': self.role
            }

            # Insérer l'utilisateur dans la base de données
            result = users_collection.insert_one(user_data)
            if result.inserted_id:
                return jsonify({
                    'status': 201,
                    'id': str(result.inserted_id),
                    'role': self.role
                }), 201
            else:
                return jsonify({
                    'status': 304, 
                    'error': 'Une erreur lors de l\'insertion'
                }), 304

        except PyMongoError as e:
            return jsonify({
                'status': 500,
                'error': f"Une erreur PyMongo s'est produite : {str(e)}"
            }), 500
        except Exception as e:
            return jsonify({
                'status': 500,
                'error': f"Une erreur inattendue s'est produite : {str(e)}"
            }), 500
    
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
    def updateFirstName(db_manager: MongoDBManager, user_id: ObjectId, new_first_name: str):
        """
            Met à jour le prénom d'un utilisateur dans la base de données.

            :param db_manager: Instance de MongoDBManager pour interagir avec la base de données.
            :param user_id: ID de l'utilisateur dont le prénom doit être mis à jour.
            :param new_first_name: Nouveau prénom à définir.
            :return: Une réponse JSON indiquant le statut de la mise à jour du prénom.
        """

        if len(new_first_name) >= 3 and new_first_name.isalpha():
            try:
                result = db_manager.get_collection('users').update_one({"_id": ObjectId(user_id)}, {"$set": {"firstName": new_first_name}})
                if result.modified_count > 0:
                    return jsonify({
                        'status': 200,
                        'message': "Donnée mise à jour avec succès."
                    }), 200
                else:
                    return jsonify({
                        'status': 400,
                        'message': "Un problème s'est produite pendant la mise à jour de la donnée."
                    }), 200
                
            except PyMongoError as e:
                return jsonify({
                    'status': 500,
                    'error': f"Une erreur PyMongo s'est produite : {str(e)}"
                }), 200
        else:
            return jsonify({
                'status': 400,
                'error': "Invalid firstName. It must be at least 3 characters long and contain only letters."
            }), 200

    @staticmethod
    def updateEmail(db_manager: MongoDBManager, user_id: ObjectId, new_email: str):
        """
            Met à jour l'adresse e-mail d'un utilisateur dans la base de données.

            :param db_manager: Instance de MongoDBManager pour interagir avec la base de données.
            :param user_id: ID de l'utilisateur dont l'adresse e-mail doit être mise à jour.
            :param new_email: Nouvelle adresse e-mail à définir.
            :return: Une réponse JSON indiquant le statut de la mise à jour de l'adresse e-mail.
        """
        
        email_regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
        if re.match(email_regex, new_email):
            print(new_email)
            try:
                result = db_manager.get_collection('users').update_one({"_id": ObjectId(user_id)}, {"$set": {"email": new_email}})
                if result.modified_count > 0:
                    return jsonify({
                        'status': 200,
                        'message': "Donnée mise à jour avec succès."
                    }), 200
                else:
                    return jsonify({
                        'status': 400,
                        'error': "Un problème s'est produite pendant la mise à jour de la donnée."
                    }), 200
            except PyMongoError as e:
                return jsonify({
                    'status': 500,
                    'error': f"Une erreur PyMongo s'est produite : {str(e)}"
                }), 200
        else:
            return jsonify({
                'status': 400,
                'error': "Invalid email format."
            }), 200

    @staticmethod
    def updatePassword(db_manager: MongoDBManager, user_id: ObjectId, old_password: str, new_password: str, confirm_password: str):
        """
            Met à jour le mot de passe d'un utilisateur dans la base de données.

            :param db_manager: Instance de MongoDBManager pour interagir avec la base de données.
            :param user_id: ID de l'utilisateur dont le mot de passe doit être mis à jour.
            :param old_password: Ancien mot de passe de l'utilisateur pour vérification.
            :param new_password: Nouveau mot de passe à définir.
            :param confirm_password: Confirmation du nouveau mot de passe.
            :return: Une réponse JSON indiquant le statut de la mise à jour du mot de passe.
        """

        # Regex pour vérifier le nouveau mot de passe
        uppercase_regex = r"[A-Z]"
        lowercase_regex = r"[a-z]"
        digit_regex = r"[0-9]"
        special_char_regex = r"[#?!@$%^&*-]"
        length_regex = r"^.{6,}$"

        if new_password != confirm_password:
            return jsonify({
                'status': 200,
                'error': "Le nouveau mot de passe et la confirmation du nouvau mot de passe ne sont pas identique."
            }), 400
             
        # Vérifie si le nouveau mot de passe respecte les critères
        if (re.search(uppercase_regex, new_password) and re.search(lowercase_regex, new_password) and
            re.search(digit_regex, new_password) and re.search(special_char_regex, new_password) and
            re.match(length_regex, new_password)):

            # Récupère le mot de passe actuel depuis la base de données
            user = db_manager.get_collection('users').find_one({"_id": ObjectId(user_id)})
            if user and 'password' in user:
                # Vérifie si l'ancien mot de passe est correct
                if check_password_hash(user['password'], old_password):
                    # Hache le nouveau mot de passe avant de l'insérer
                    hashed_new_password = generate_password_hash(new_password)
                    try:
                        # Met à jour le mot de passe dans la base de données
                        result = db_manager.get_collection('users').update_one({"_id": ObjectId(user_id)}, {"$set": {"password": hashed_new_password}})
                        if result.modified_count > 0:
                            return jsonify({
                                'status': 200,
                                'message': "Mot de passe mis à jour avec succès."
                            }), 200
                        else:
                            return jsonify({
                                'status': 400,
                                'message': "Aucune mise à jour n'a été effectuée."
                            }), 200
                    except PyMongoError as e:
                        return jsonify({
                            'status': 500,
                            'error': f"Une erreur PyMongo s'est produite : {str(e)}"
                        }), 200
                else:
                    return jsonify({
                        'status': 400,
                        'error': "L'ancien mot de passe est incorrect."
                    }), 200
            else:
                return jsonify({
                    'status': 404,
                    'error': "Utilisateur non trouvé."
                }), 200
        else:
            return jsonify({
                'status': 400,
                'error': "Le nouveau mot de passe ne respecte pas les exigences."
            }), 200

    @staticmethod
    def deleteUser(db_manager: MongoDBManager, user_id: ObjectId):
        """
            Supprime l'utilisateur et ses entrées dans les collections 'tickets' et 'badges'.

            :param db_manager: Instance de MongoDBManager pour interagir avec la base de données.
            :param user_id: ID de l'utilisateur à supprimer.
        """

        try:
            # Supprime l'utilisateur de la collection 'users'
            result = db_manager.get_collection('users').delete_one({"_id": ObjectId(user_id)})
            if result.deleted_count > 0:
                # Supprime les entrées correspondantes dans les collections 'tickets' et 'badges'
                db_manager.get_collection('tickets').delete_many({"user_id": str(user_id)})
                db_manager.get_collection('badges').delete_many({"user_id": str(user_id)})
            else:
                return jsonify({
                    'status': 400,
                    'error': "Aucun compte n'a été supprimé."
                }), 200
        except PyMongoError as e:
            return jsonify({
                'status': 500,
                'error': f"Une erreur PyMongo s'est produite : {str(e)}"
            }), 200

        return jsonify({
            'status': 200,
        }), 200

    @staticmethod
    def getGeneralsInfosUser(db_manager: MongoDBManager, user_id: ObjectId):
        """
            Récupère des informations générales sur un utilisateur, notamment le nombre de tickets achetés ce mois-ci
            et le QR Code du dernier ticket acheté.

            Args:
                db_manager (MongoDBManager): Le gestionnaire de base de données MongoDB.
                user_id (str): L'identifiant de l'utilisateur pour lequel récupérer les informations.

            Returns:
                tuple: Un tuple contenant un objet JSON et un code HTTP.

                Le JSON contient les informations suivantes :
                - 'status' (int): Le code de statut de la réponse.
                - 'ticket_count' (int): Le nombre de tickets achetés ce mois-ci par l'utilisateur.
                - 'last_ticket_qrcode' (dict): Les informations du dernier ticket acheté sous forme de QR Code en Base64.
                
                Le code HTTP indique le succès ou l'échec de la requête.
        """

        try:
            tickets_collection = db_manager.get_collection('tickets')
        except PyMongoError as e:
            return jsonify({
                'status': 500,
                'error': f"Une erreur PyMongo s'est produite : {str(e)}"
            }), 500

        # Obtenir la date de début du mois actuel en UTC
        today_utc = datetime.datetime.utcnow()
        first_day_of_month_utc = today_utc.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        try:
            # Compter les tickets de l'utilisateur achetés ce mois-ci
            ticket_count = tickets_collection.count_documents({
                'user_id': user_id,
                'date_achat': {'$gte': first_day_of_month_utc}
            })

            # Récupérer le dernier ticket acheté
            last_ticket = tickets_collection.find_one(
                {'user_id': user_id},
                sort=[('date_achat', -1)]
            )
            if last_ticket:
                id = str(last_ticket.get('_id', 'N/A'))
                date_achat = last_ticket.get('date_achat', 'N/A')
                type = last_ticket.get('type', 'N/A')
                validite = last_ticket.get('validite', 'N/A')
                etat = last_ticket.get('etat', 'N/A')
                nb_scannes = last_ticket.get('nb_scannes', '0')
                
                last_ticket_qrcode = QRCode.create_qr_code_with_info(id, date_achat, type, validite, etat, nb_scannes)
            else:
                last_ticket_qrcode = None
                
            
            return jsonify({
                'status': 200,
                'ticket_count': ticket_count,
                'last_ticket_qrcode': last_ticket_qrcode
            }), 200
        except PyMongoError as e:
            return jsonify({
                'status': 500,
                'error': f"Une erreur PyMongo s'est produite : {str(e)}"
            }), 500
         
    @staticmethod
    def getAllTicketsUser(db_manager: MongoDBManager, user_id: ObjectId):
        """
            Récupère tous les tickets associés à un utilisateur donné.

            :param db_manager: Instance de MongoDBManager pour interagir avec la base de données.
            :param user_id: ID de l'utilisateur dont on veut récupérer les tickets.
            :return: Liste des tickets de l'utilisateur ou une liste vide si aucun ticket n'est trouvé.
        """
        
        # Récuperation des tickets de l'utilisateur
        try:
            tickets_collection = db_manager.get_collection('tickets')
            tickets = tickets_collection.find({'user_id': user_id})
            
            # Convertir chaque ticket en un dictionnaire et changer les ObjectId en strings
            tickets_list = []
            for ticket in tickets:
                ticket_dict = dict(ticket)
                # Convertir l'ObjectId en string
                ticket_dict['_id'] = str(ticket_dict['_id'])
                
                # Générer le QR Code en Base64 pour le ticket
                qr_code_data = QRCode.create_qr_code_with_info(ticket_dict['_id'], ticket_dict['date_achat'], ticket_dict['type'], ticket_dict['validite'], ticket_dict['etat'], ticket_dict['nb_scannes'])
                # J'ajoute dans le dict le qr_code ainsi que les info mise dans le qr code sous forme texte. (redondante)
                ticket_dict['qr_code'] = qr_code_data['qr_code_base64']
                ticket_dict['qr_code_info'] = qr_code_data['ticket_info']

                tickets_list.append(ticket_dict)

        except Exception as e:
            return jsonify({
                'status': 500,
                'error': f"Erreur lors de la récupération des tickets: {e}"
            }), 500
            
        # Récuperation des badges de l'utilisateur
        try:
            badges_collection = db_manager.get_collection('badges')
            badges = badges_collection.find({'user_id': user_id})
            
            badges_list = []
            for badge in badges:
                badge_dict = dict(badge)

                badge_dict['_id'] = str(badge_dict['_id'])
                
                qr_code_data = QRCode.create_qr_code_with_info(badge_dict['_id'], badge_dict['date_achat'], badge_dict['type'], badge_dict['validite'], badge_dict['etat'], badge_dict['nb_scannes'])
                
                badge_dict['qr_code'] = qr_code_data['qr_code_base64']
                badge_dict['qr_code_info'] = qr_code_data['ticket_info']

                badges_list.append(badge_dict)

        except Exception as e:
            return jsonify({
                'status': 500,
                'error': f"Erreur lors de la récupération des tickets: {e}"
            }), 500

        return jsonify({
            'status': 200,
            'ticket_count': len(tickets_list),
            'tickets': tickets_list,
            'badge_count': len(badges_list),
            'badges': badges_list
        }), 200

    
    @staticmethod
    def login(db_manager: MongoDBManager, email:str, password:str):
        """
            Authentifie un utilisateur en vérifiant l'email et le mot de passe dans la base de données.

            :param db_manager: Instance de MongoDBManager pour interagir avec la base de données.
            :param email: Adresse e-mail de l'utilisateur à authentifier.
            :param password: Mot de passe de l'utilisateur à vérifier.
            :return: Une réponse JSON avec le statut HTTP approprié.
        """

        user = db_manager.get_collection('users').find_one({"email": email})
        if user:
            # Vérification du mot de passe haché
            if check_password_hash(user['password'], password):
                return jsonify({
                    'status': 200,
                    'id': str(user['_id']),
                    'first_name': user['firstName'],
                    'email': user['email'],
                    'role': user['role']
                }), 200
        return jsonify({
            'status': 401,
        }), 401
