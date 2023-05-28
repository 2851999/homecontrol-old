# This script can be used to add a user with a given username and password

import argparse
from getpass import getpass

from homecontrol.api.authentication.structs import UserGroup
from homecontrol.api.authentication.user_manager import UserManager
from homecontrol.api.config import APIConfig
from homecontrol.api.database.client import APIDatabaseClient

parser = argparse.ArgumentParser(
    prog="add_user", description="Adds a user to the homecontrol database"
)
parser.add_argument("username", help="Username of the user to add")
user_group_options = [group.value for group in UserGroup]
parser.add_argument(
    "--group",
    default="default",
    choices=user_group_options,
    help=f"User group the user should have permissions for",
)
args = parser.parse_args()

username = args.username
password = getpass("Enter a password: ")
password2 = getpass("Re-enter the password: ")
group = args.group

if password != password2:
    print("Password's don't match!")
    raise SystemExit(1)

print(f"Adding user '{username}' to the database")

user_manager = UserManager(APIConfig(), APIDatabaseClient())
user_manager.add_user(username, password, group)
