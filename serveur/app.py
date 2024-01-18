"""
|
|   This file contains all the configuration settings for the server of the project.
|
|   Author: Mahmoud ILLOURMANE
|   Date: January 18, 2024
|
|
"""

# Importation des packages nécessaires au bon fonctionnement du projet Flask
from flask import Flask

"""
|
| App Configurations
|
"""

app = Flask(__name__)

# Activation du mode de débogage
app.debug = True

# Importation du fichier api.py
from routes.api import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
