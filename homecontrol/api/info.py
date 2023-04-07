from flask import Blueprint

from homecontrol.api.helpers import (
    response,
)
from homecontrol.api.structs import APIInfo
from homecontrol.helpers import ResponseStatus, object_to_dict
from homecontrol.version import __version__


info_api = Blueprint("info_api", __name__)


@info_api.route("/info", methods=["GET"])
def get_info():
    """
    Returns some info about this instance of homecontrol
    """

    info = APIInfo(version=__version__)

    return response(object_to_dict(info), ResponseStatus.OK)