from flask import jsonify
from pymongo.errors import PyMongoError
from bson import ObjectId

from datetime import datetime, timedelta
import json

from src.classes.mongoDb import MongoDBManager
from src.classes.qrCode import QRCode

class Badge:
    def __init__(self, db_manager:MongoDBManager, date_achat:datetime, validite:datetime, etat='J', nb_scannes=0, id=None, user_id=None):
        """
            Classe représentant un badge dans le système.

            Attributes:
                id (str): L'identifiant unique du badge.
                user_id (str): L'identifiant de l'utilisateur associé au badge.
                db_manager (MongoDBManager): Le gestionnaire de la base de données MongoDB.
                date_achat (datetime): La date d'achat du badge.
                type (str): Le type de badge (toujours "Badge").
                validite (datetime): La date de validité du badge.
                etat (str): L'état du badge (par défaut "J" pour actif).
                nb_scannes (int): Le nombre de fois que le badge a été scanné (par défaut 0).

            Methods:
                createBadge(self)
                    Crée un nouveau badge dans la base de données.
                
                scannerBadge(self, badge_id: str)
                    Scanner le badge avec l'ID donné.
        """
        
        self.id = id
        self.user_id = user_id
        self.db_manager = db_manager
        self.date_achat = date_achat
        self.type = "Badge"
        self.validite = validite
        self.etat = etat
        self.nb_scannes = nb_scannes
            
    def createBadge(self):
        """
            Crée un nouveau badge dans la base de données.

            Returns:
                tuple: Un tuple contenant la réponse JSON et le code de statut HTTP.
                    - Si le badge est créé avec succès, retourne (json_response, 201).
                    - Si une erreur survient lors de l'insertion du badge, retourne (json_response, 304).
                    - Si une erreur PyMongo se produit, retourne (json_response, 500).

            Raises:
                None
        """
        
        try:
            badges_collection = self.db_manager.get_collection('badges')
        except PyMongoError as e:
            return jsonify({
                'status': 500,
                'error': f"Une erreur PyMongo s'est produite : {str(e)}"
            }), 500
            
        # Créer le document utilisateur
        new_badge = {
            'user_id': self.user_id,
            'date_achat': self.date_achat,
            'type': self.type,
            'validite': self.validite,
            'etat': self.etat,
            'nb_scannes': self.nb_scannes
        }
        
        try:
            # Insérer l'utilisateur dans la base de données
            result = badges_collection.insert_one(new_badge)
            
            if result.inserted_id:
                json_data = {
                    'id': str(result.inserted_id),
                    'validite': str(self.validite),
                    'type': self.type
                }
                
                qr_code_base64 = QRCode.create_qr_code_from_json(json.dumps(json_data))
                return jsonify({
                    'status': 201,
                    'message': 'Badge créée avec succès.',
                    'id': str(result.inserted_id),
                    'date_achat': self.date_achat,
                    'type': self.type,
                    'validite': self.validite,
                    'qr_code_base64': qr_code_base64
                }), 201
            else:
                return jsonify({
                    'status': 304, 
                    'error': 'Une erreur lors de l\'insertion du badge.'
                }), 304
        except PyMongoError as e:
            return jsonify({
                'status': 500,
                'error': f"Une erreur PyMongo s'est produite : {str(e)}"
            }), 500
            
    @staticmethod
    def scannerBadge(badge_id:str, db_manager: MongoDBManager):
        """
            Scanner un badge dans la base de données.

            Cette méthode prend en entrée l'ID du badge à scanner et un gestionnaire de base de données MongoDB.

            Args:
                badge_id (str): L'ID du badge à scanner.
                db_manager (MongoDBManager): Le gestionnaire de la base de données MongoDB.

            Returns:
                tuple: Un tuple contenant la réponse JSON et le code de statut HTTP.
        """
    
        # Obtenir la référence à la collection 'badges'
        badges_collection = db_manager.get_collection('badges')
        
        badge = badges_collection.find_one({'_id': ObjectId(badge_id)})
        
        if badge:
            # Je vérifie si la date de validité du badge est supérieure à la date actuelle
            if datetime.now() < badge['validite']:
                # Incrémentation de la valeur nb_scannes de 1
                update_data = {'$inc': {'nb_scannes': 1}}
                # Initialisation de '$set' pour éviter d'écraser les modifications précédentes
                update_data['$set'] = {}

                # Deuxième vérification : l'état du badge
                if badge['etat'] == "N":
                    # Mise à jour de l'état à "V"
                    update_data['$set']['etat'] = 'V'
                    # Mise à jour de la validité pour 30 jours
                    new_validite = datetime.now() + timedelta(days=30)
                    # Mise à jour de la validité dans '$set'
                    update_data['$set']['validite'] = new_validite
                
                # Mise à jour du badge dans la base de données
                badges_collection.update_one({'_id': ObjectId(badge_id)}, update_data)
                
                return jsonify({
                    'status': 200,
                    'message': 'Porte Ouverte.',
                }), 200 
            else:
                update_data = {'$set': {'etat': 'P'}}
                badges_collection.update_one({'_id': ObjectId(badge_id)}, update_data)
                
                return jsonify({
                    'status': 410,
                    'error': 'Le badge est périmé.',
                }), 200
            
        else:
            return jsonify({
                'status': 404 ,
                'error': 'Badge non trouvé.',
            }), 200     