import paho.mqtt.client as mqtt
import json
from routes.api import sendQrCodeInfosToServer

class MQTTSubscriber:

    def __init__(self):
        """
            Constructeur de la classe MQTTSubscriber.

            Initialise un client MQTT avec un nom "PythonSubscriber", configure les méthodes de rappel
            et active le logging pour le débogage.
        """

        self.client = mqtt.Client("PythonSubscriber")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        # Active le logging pour le débogage
        self.client.enable_logger()

    def on_connect(self, client, userdata, flags, rc):
        """
            Méthode de rappel appelée lors de la connexion à un broker MQTT.

            :param client: Objet client MQTT.
            :param userdata: Données utilisateur (optionnel).
            :param flags: Drapeaux de connexion (optionnel).
            :param rc: Code de retour de la connexion (0 si la connexion réussie).
        """
        
        if rc == 0:
            # print("Connecté avec succès au broker MQTT")
            client.subscribe("check/transport")
        else:
            print(f"Échec de la connexion avec le code {rc}")

    def on_message(self, client, userdata, msg):
        """
            Méthode de rappel appelée lors de la réception d'un message MQTT.

            :param client: Objet client MQTT.
            :param userdata: Données utilisateur (optionnel).
            :param msg: Objet message contenant le topic et le payload du message reçu.
        """
        
        # print(f"Message reçu -> Topic: {msg.topic}, Payload: {msg.payload}")
        try:
            qrCodeInfos = json.loads(msg.payload)
            sendQrCodeInfosToServer(qrCodeInfos)
        except json.JSONDecodeError:
            print("Erreur lors de la décodification du message:", msg.payload)

    def start(self):
        """
            Méthode pour démarrer un abonné MQTT.

            Crée un client MQTT, configure les méthodes de rappel, active le logging pour le débogage,
            établit la connexion avec un broker MQTT local sur le port 1883, et démarre la boucle du client MQTT
            en arrière-plan pour la gestion des messages.
        """
        
        # Utilisation de connect_async pour une gestion non bloquante de la connexion
        self.client.connect_async("localhost", 1883, 60)
        self.client.loop_start()