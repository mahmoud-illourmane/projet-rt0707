import paho.mqtt.client as mqtt

from src.classes.tools import write_log

class MQTTClient:
    def __init__(self, client_id):
        """
            Initialise un client MQTT avec l'identifiant spécifié.
            Args:
                client_id (str): L'identifiant unique du client MQTT.
            Cette méthode crée une instance de client MQTT et établit une connexion
            au broker MQTT sur le nom de service défini dans docker-compose (brokerMqtt)
            sur le port 1883 avec un délai d'attente pour une connexion de 60 secondes.
        """
        self.client = mqtt.Client(client_id)
        # En Vm
        try:
            self.client.connect("brokerMqtt", 1883, 60)
        except Exception as e:
            write_log(f"Erreur lors de la connexion au BrokerMqtt: {str(e)}")
        
        # En Local
        # self.client.connect("localhost", 1883, 60)
        
    def publish(self, topic, message):
        """
            Publie un message sur un topic spécifié.
        """
        try:
            self.client.publish(topic, message)
        except Exception as e:
            write_log(f"Erreur lors de la publication sur le topic {topic}: {str(e)}")
