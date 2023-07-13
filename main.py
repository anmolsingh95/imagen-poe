# Welcome to the Poe API tutorial. The starter code provided provides you with a quick way to get
# a bot running. By default, the starter code uses the EchoBot, which is a simple bot that echos
# a message back at its user and is a good starting point for your bot, but you can
# comment/uncomment any of the following code to try out other example bots.

import json
import os

import firebase_admin
import openai
from fastapi_poe import make_app
from firebase_admin import credentials
from modal import Image, Secret, Stub, asgi_app

from imagen_bot import ImaGenBot

image = Image.debian_slim().pip_install_from_requirements("requirements.txt")
stub = Stub("imagen-poe")


@stub.function(image=image, secret=Secret.from_name("imagen-poe"))
@asgi_app()
def fastapi_app():
    openai.api_key = os.environ["OPENAI_API_KEY"]
    cred = credentials.Certificate(json.loads(os.environ["FIREBASE_KEY_JSON"]))
    firebase_admin.initialize_app(
        cred,
        {
            "storageBucket": "imagen-poe.appspot.com",
            "databaseURL": "https://imagen-poe-default-rtdb.firebaseio.com/",
        },
    )
    bot = ImaGenBot()
    POE_API_KEY = os.environ["POE_API_KEY"]
    app = make_app(bot, api_key=POE_API_KEY)
    return app
