import json
import os

import firebase_admin
import openai
from fastapi_poe import make_app
from firebase_admin import credentials
from modal import Image, Secret, Stub, asgi_app

from imagen_bot import ImaGenBot

image = Image.debian_slim().pip_install_from_requirements("requirements.txt")
stub = Stub("imagen-poe-app")


@stub.function(image=image, secret=Secret.from_name("imagen-poe-secret"))
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
    app = make_app(bot, access_key=os.environ["POE_ACCESS_KEY"])
    return app
