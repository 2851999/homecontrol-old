from flask import Flask

from flask_cors import CORS

from homecontrol.api.config import APIConfig
from homecontrol.api.helpers import authenticated, response_message
from homecontrol.api.aircon import aircon_api
from homecontrol.api.hue import hue_api
from homecontrol.api.home import home_api
from homecontrol.api.monitoring import construct_monitor_api_blueprint

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

# Load the API config
config = APIConfig()
auth_config = config.get_auth()

app.config["APIAuthConfig"] = auth_config

# Register blueprints
app.register_blueprint(aircon_api)
app.register_blueprint(hue_api)
app.register_blueprint(home_api)

# Monitoring
app.register_blueprint(construct_monitor_api_blueprint())


@app.route("/")
@authenticated
def root():
    """
    Default root
    """
    return response_message("OK: Authorised", 200)


if __name__ == "__main__":
    app.run()
