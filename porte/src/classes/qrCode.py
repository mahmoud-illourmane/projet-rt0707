import base64
import io
from PIL import Image
from pyzbar.pyzbar import decode
import json

class QRCode:

    @staticmethod
    def decode_json_from_qr_code(base64_qr_code):
        """
            Décode un QR Code encodé en Base64 et extrait les données JSON.

            Args:
                base64_qr_code (str): Image QR Code encodée en Base64.

            Returns:
                dict: Données JSON extraites du QR Code.

            Exemple:
                qr_code_base64 = <Votre image QR Code en Base64>
                
                json_data = QRCode.decode_json_from_qr_code(qr_code_base64)
                
                print(json_data)
        """

        # Convertir Base64 en image
        image_data = base64.b64decode(base64_qr_code)
        image = Image.open(io.BytesIO(image_data))

        # Décoder le QR Code
        decoded_data = decode(image)

        # Extraire les données JSON du QR Code
        if decoded_data:
            json_data = decoded_data[0].data.decode("utf-8")
            print(json_data)
            return json.loads(json_data)

        return None