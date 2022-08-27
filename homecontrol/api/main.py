from flask import Flask

from flask_cors import CORS

from homecontrol.api.config import APIConfig
from homecontrol.api.helpers import authenticated, response_message

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

# Load the API config
config = APIConfig()
auth_config = config.get_auth()

app.config["APIAuthInfo"] = auth_config


@app.route("/")
@authenticated
def root():
    """
    Default root
    """
    return response_message("OK: Authorised", 200)


if __name__ == "__main__":
    app.run()
