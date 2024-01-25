import qrcode, io, base64, json

class QRCode:

    @staticmethod
    def create_qr_code_from_json(json_data):
        """
            Crée un QR Code à partir d'une chaîne JSON et retourne l'image en Base64.

            Args:
                json_data (str): Données JSON à encoder dans le QR Code.

            Returns:
                str: Image QR Code encodée en Base64.
            
            Exemple : 
                json_data = json.dumps({
                    'id': id,
                    'date_achat': date_achat,
                    'type': type
                })

                qr_code_base64 = QRCode.create_qr_code_from_json(json_data)
                
                <img src="data:image/png;base64,qr_code_base64" />
        """

        # Convertit la chaîne JSON en dictionnaire
        data_dict = json.loads(json_data)
        
        # Création du QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data_dict)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

        return img_base64  

    @staticmethod
    def create_qr_code_with_info(id, date_achat, type, validite, etat, nb_scannes):
        """
            Crée un QR Code avec les informations du ticket et retourne l'image en Base64 
            et les informations de création.

            Args:
                id (str): ID du ticket.
                date_achat (str): Date d'achat du ticket.
                type (str): Type de ticket.
                validite (str): Date de validité du ticket.
                etat (str): État du ticket.

            Returns:
                dict: Dictionnaire contenant l'image du QR Code en Base64 et les informations de création.
        """
        
        # Préparation des données du ticket
        ticket_info = {
            'id': id,
            'date_achat': date_achat.strftime('%Y-%m-%d %H:%M:%S'),
            'type': type,
            'validite': validite.strftime('%Y-%m-%d %H:%M:%S'),
            'etat': etat,
            'nb_scannes': nb_scannes
        }

        # Convertit les données du ticket en chaîne JSON
        json_data = json.dumps(ticket_info)

        # Création du QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Conversion de l'image en Base64
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

        # Retourne l'image en Base64 et les informations du ticket
        return {
            'qr_code_base64': img_base64,
            'ticket_info': ticket_info
        }