from flask import Flask
from flask_cors import CORS

from homecontrol.api.aircon import aircon_api
from homecontrol.api.auth import auth_api
from homecontrol.api.authentication.user_manager import UserManager
from homecontrol.api.config import APIConfig
from homecontrol.api.database.client import APIDatabaseClient
from homecontrol.api.exceptions import APIError
from homecontrol.api.helpers import authenticated, response_message
from homecontrol.api.home import home_api
from homecontrol.api.hue import hue_api
from homecontrol.api.info import info_api
from homecontrol.api.monitoring import construct_monitor_api_blueprint

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

# Load the API config
config = APIConfig()
auth_config = config.get_auth()

# TODO: Unify with AuthManager or something
app.config["APIAuthConfig"] = auth_config
app.config["UserManager"] = UserManager(config, APIDatabaseClient())

# Register blueprints
app.register_blueprint(auth_api)
app.register_blueprint(aircon_api)
app.register_blueprint(hue_api)
app.register_blueprint(home_api)
app.register_blueprint(info_api)

# Monitoring
app.register_blueprint(construct_monitor_api_blueprint())


@app.route("/")
@authenticated
def root():
    """
    Default root
    """
    return response_message("OK: Authorised", 200)


@app.errorhandler(APIError)
def handle_api_error(err: APIError):
    """
    Return error messages when an APIError occurs
    """
    return response_message(err.message, err.status_code)


if __name__ == "__main__":
    app.run()
