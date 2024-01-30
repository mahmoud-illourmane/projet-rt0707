from datetime import datetime

class Verif:
    @staticmethod
    def qrCodeVerifLocal(qrCodeInfos):
        """
            Vérifie si le ticket ou badge est valide en comparant les dates d'achat et de validité avec la date et l'heure actuelles.

            :param qrCodeInfos: Dictionnaire contenant les informations du QR Code, y compris les dates d'achat et de validité.
            :return: True si le ticket/badge est valide, False sinon.
        """
        
        # Extraction des dates d'achat et de validité à partir de qrCodeInfos
        date_achat = datetime.strptime(qrCodeInfos['date_achat'], '%Y-%m-%d %H:%M:%S')
        date_validite = datetime.strptime(qrCodeInfos['validite'], '%Y-%m-%d %H:%M:%S')
        
        # Obtention de la date et de l'heure actuelles
        maintenant = datetime.now()
        
        # Vérification de la validité du ticket/badge
        if date_achat <= maintenant <= date_validite:
            return True
        else:
            return False
