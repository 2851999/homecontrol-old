import argparse
from abc import abstractmethod
from getpass import getpass
from typing import List

from homecontrol.api.authentication.structs import UserGroup
from homecontrol.api.authentication.user_manager import UserManager
from homecontrol.api.config import APIConfig
from homecontrol.api.database.client import APIDatabaseClient


class Command:
    name: str
    help_str: str

    def __init__(self, name: str, help_str: str) -> None:
        self.name = name
        self.help_str = help_str

    @abstractmethod
    def add_arguments(self, parser):
        pass

    @abstractmethod
    def run(self, args: argparse.Namespace):
        pass


class Command_InitDB(Command):
    def __init__(self) -> None:
        super().__init__(
            name="init-db", help_str="Initialises the homecontrol database"
        )

    def add_arguments(self, parser):
        pass

    def run(self, args: argparse.Namespace):
        print("Initialising the homecontrol database...")
        database_client = APIDatabaseClient()
        with database_client.connect() as conn:
            conn.init_db()
        print("Done!")


def add_subcommands(parser, subcommands: List[Command]):
    subparsers = parser.add_subparsers()

    for command in subcommands:
        command_parser = subparsers.add_parser(command.name, help=command.help_str)
        command_parser.set_defaults(func=command.run)
        command.add_arguments(command_parser)


class Command_Add_User(Command):
    def __init__(self) -> None:
        super().__init__(
            name="user", help_str="Adds a user to the homecontrol database"
        )

    def add_arguments(self, parser):
        user_group_options = [group.value for group in UserGroup]

        parser.add_argument("username", help="Username of the user to add")
        parser.add_argument(
            "--group",
            default="default",
            choices=user_group_options,
            help=f"User group the user should have permissions for",
        )

    def run(self, args: argparse.Namespace):
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


class Command_Add(Command):
    def __init__(self) -> None:
        super().__init__(name="add", help_str="Add something to homecontrol")

    def add_arguments(self, parser):
        add_subcommands(parser, [Command_Add_User()])

    def run(self, args: argparse.Namespace):
        pass


def main():
    """Entrypoint"""

    parser = argparse.ArgumentParser(prog="homecontrol-management")
    add_subcommands(parser, [Command_InitDB(), Command_Add()])

    # Run
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
