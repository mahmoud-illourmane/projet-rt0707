import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, client_id):
        """
            Initialise un client MQTT avec l'identifiant spécifié.

            Args:
                client_id (str): L'identifiant unique du client MQTT.

            Cette méthode crée une instance de client MQTT et établit une connexion au broker MQTT sur localhost
            (adresse IP 127.0.0.1) sur le port 1883 avec un délai de 60 secondes.
        """

        self.client = mqtt.Client(client_id)
        self.client.connect("localhost", 1883, 60)
    
    def publish(self, topic, message):
        """
            Publie un message sur un topic spécifié.
        """
        
        self.client.publish(topic, message)
