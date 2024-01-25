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
