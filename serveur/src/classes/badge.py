from flask import jsonify
from pymongo.errors import PyMongoError
import datetime, json

from src.classes.mongoDb import MongoDBManager
from src.classes.qrCode import QRCode

class Badge:
    def __init__(self, db_manager:MongoDBManager, date_achat:datetime, validite:datetime, etat='J', id=None, user_id=None):
        self.id = id
        self.user_id = user_id
        self.db_manager = db_manager
        self.date_achat = date_achat
        self.type = 'Badge'
        self.validite = validite
        self.etat = etat
            
    def createBadge(self):
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
            'etat': self.etat
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
            
        
        