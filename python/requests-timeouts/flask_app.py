from flask import Flask
import time
from flask import Response


app = Flask(__name__)

@app.route("/")
def hello_world():
    time.sleep(20)
    return Response("Gateway timeout", status=504)
    