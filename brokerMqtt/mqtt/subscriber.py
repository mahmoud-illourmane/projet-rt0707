import paho.mqtt.client as mqtt
import json
from routes.api import sendQrCodeInfosToServer

class MQTTSubscriber:

    def __init__(self):
        self.client = mqtt.Client("PythonSubscriber")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        # Active le logging pour aider au débogage
        self.client.enable_logger()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            # print("Connecté avec succès au broker MQTT")
            client.subscribe("check/transport")
        else:
            print(f"Échec de la connexion avec le code {rc}")

    def on_message(self, client, userdata, msg):
        # print(f"Message reçu -> Topic: {msg.topic}, Payload: {msg.payload}")
        try:
            qrCodeInfos = json.loads(msg.payload)
            sendQrCodeInfosToServer(qrCodeInfos)
        except json.JSONDecodeError:
            print("Erreur lors de la décodification du message:", msg.payload)

    def start(self):
        # Utilisation de connect_async pour une gestion non bloquante de la connexion
        self.client.connect_async("localhost", 1883, 60)
        self.client.loop_start()