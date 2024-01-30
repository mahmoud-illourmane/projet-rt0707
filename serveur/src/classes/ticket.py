from flask import jsonify
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId

import json
from datetime import datetime, timedelta

from src.classes.mongoDb import MongoDBManager
from src.classes.qrCode import QRCode

class Ticket:
    def __init__(self, db_manager:MongoDBManager, date_achat:datetime, type:str, validite:datetime, etat='N', nb_scannes=0, id=None, user_id=None):
        """
            Classe représentant un ticket dans le système.

            Attributes:
                id (str): L'identifiant unique du ticket.
                user_id (str): L'identifiant de l'utilisateur associé au ticket.
                db_manager (MongoDBManager): Le gestionnaire de la base de données MongoDB.
                date_achat (datetime): La date d'achat du ticket.
                type (str): Le type de ticket (par exemple, "1J" ou "2H").
                validite (datetime): La date de validité du ticket.
                etat (str): L'état du ticket (par défaut "N" pour non validé).
                nb_scannes (int): Le nombre de fois que le ticket a été scanné (par défaut 0).

            Methods:
                createTicket(self)
                    Crée un nouveau ticket dans la base de données.
                
                scannerTicket(self, ticket_id: str)
                    Scanner le ticket avec l'ID donné.
        """
    
        self.id = id
        self.user_id = user_id
        self.db_manager = db_manager
        self.date_achat = date_achat
        self.type = type
        self.validite = validite
        self.etat = etat
        self.nb_scannes = nb_scannes
    
    def createTicket(self):
        """
            Crée un nouveau ticket dans la base de données.

            Cette méthode crée un nouveau ticket en utilisant les informations fournies dans l'objet actuel.
            
            Returns:
                tuple: Un tuple contenant la réponse JSON et le code de statut HTTP.
                    - Si le ticket est créé avec succès, retourne (json_response, 201).
                    - Si une erreur survient lors de l'insertion du ticket, retourne (json_response, 304).
                    - Si une erreur PyMongo se produit, retourne (json_response, 500).
        """

        try:
            tickets_collection = self.db_manager.get_collection('tickets')
        except PyMongoError as e:
            return jsonify({
                'status': 500,
                'error': f"Une erreur PyMongo s'est produite : {str(e)}"
            }), 500
            
        print('user id dans ticket :', self.user_id)
        # Créer le document utilisateur
        new_ticket = {
            'user_id': self.user_id,
            'date_achat': self.date_achat,
            'type': self.type,
            'validite': self.validite,
            'etat': self.etat,
            'nb_scannes': self.nb_scannes
        }
        
        try:
            # Insérer l'utilisateur dans la base de données
            result = tickets_collection.insert_one(new_ticket)
            
            if result.inserted_id:
                json_data = {
                    'id': str(result.inserted_id),
                    'date_achat': str(self.date_achat),
                    'type': self.type
                }
                
                qr_code_base64 = QRCode.create_qr_code_from_json(json.dumps(json_data))
                return jsonify({
                    'status': 201,
                    'message': 'Ticket créée avec succès.',
                    'id': str(result.inserted_id),
                    'date_achat': self.date_achat,
                    'type': self.type,
                    'validite': self.validite,
                    'qr_code_base64': qr_code_base64
                }), 201
            else:
                return jsonify({
                    'status': 304, 
                    'error': 'Une erreur lors de l\'insertion du ticket.'
                }), 304
        except PyMongoError as e:
            return jsonify({
                'status': 500,
                'error': f"Une erreur PyMongo s'est produite : {str(e)}"
            }), 500
            
    @staticmethod
    def scannerTicket(ticket_id:str, db_manager:MongoDBManager):
        """
            Scanner un ticket dans la base de données.

            Cette méthode prend en entrée l'ID du ticket à scanner et un gestionnaire de base de données MongoDB.

            Args:
                ticket_id (str): L'ID du ticket à scanner.
                db_manager (MongoDBManager): Le gestionnaire de la base de données MongoDB.

            Returns:
                tuple: Un tuple contenant la réponse JSON et le code de statut HTTP.
                    - Si le ticket est scanné avec succès, retourne (json_response, 200).
                    - Si le ticket est périmé, retourne (json_response, 410).
                    - Si le ticket n'est pas trouvé, retourne (json_response, 404).
        """
    
        # J'obtiens la référence à la collection 'tickets'
        tickets_collection = db_manager.get_collection('tickets')
        
        # Je convertis l'ID du ticket en ObjectId pour la requête MongoDB
        ticket = tickets_collection.find_one({'_id': ObjectId(ticket_id)})
        
        if ticket:
            # Je vérifie si la date de validité du ticket est supérieure à la date actuelle
            if datetime.now() < ticket['validite']:
                # Incrémentation de la valeur nb_scannes de 1
                update_data = {'$inc': {'nb_scannes': 1}}
                # Initialisation de '$set' pour éviter d'écraser les modifications précédentes
                update_data['$set'] = {}
        
                # Deuxième vérification : l'état du ticket
                if ticket['etat'] == "N":
                    # Mise à jour de l'état à "V"
                    update_data['$set']['etat'] = 'V'

                    # Troisième vérification : le type du ticket
                    if ticket['type'] == "1J":
                        # Mise à jour de la validité pour 24 heures
                        new_validite = datetime.now() + timedelta(hours=24)
                    elif ticket['type'] == "2H":
                        # Mise à jour de la validité pour 2 heures
                        new_validite = datetime.now() + timedelta(hours=2)
                    # Mise à jour de la validité dans '$set'
                    update_data['$set']['validite'] = new_validite
                            
                # Mise à jour du ticket dans la base de données
                tickets_collection.update_one({'_id': ObjectId(ticket_id)}, update_data)
                
                return jsonify({
                    'status': 200,
                    'message': 'Porte Ouverte.',
                }), 200 
            else:
                update_data = {'$set': {'etat': 'P'}}
                tickets_collection.update_one({'_id': ObjectId(ticket_id)}, update_data)
                
                return jsonify({
                    'status': 410,
                    'error': 'Le ticket est périmé.',
                }), 410
        else:
            return jsonify({
                'status': 404 ,
                'error': 'Ticket non trouvé.',
            }), 404 
    
    