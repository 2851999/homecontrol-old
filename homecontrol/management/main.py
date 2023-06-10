import argparse
from abc import abstractmethod
from getpass import getpass
from typing import List
from uuid import uuid4

from homecontrol.aircon.manager import ACManager
from homecontrol.api.aircon.state import save_state
from homecontrol.api.authentication.structs import UserGroup
from homecontrol.api.authentication.user_manager import UserManager
from homecontrol.api.config import APIConfig
from homecontrol.api.consts import ICON_NAMES
from homecontrol.api.database.client import APIDatabaseClient
from homecontrol.api.structs import RoomState
from homecontrol.hue.hue import HueBridge
from homecontrol.hue.manager import HueManager


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


class Command_Add_RoomState(Command):
    def __init__(self) -> None:
        super().__init__(
            name="room-state", help_str="Adds a RoomState to the homecontrol database"
        )

    def add_arguments(self, parser):
        parser.add_argument("name", help="Name of the room state to add")
        parser.add_argument("icon", help="Icon of the room state to add")
        parser.add_argument("room_name", help="Name of the room the state will act on")
        parser.add_argument(
            "--ac_device_name", help="Name of the aircon device the state acts on"
        )
        parser.add_argument(
            "--hue_scene_name", help="Name of the hue scene this should activate"
        )
        parser.add_argument(
            "--broadlink_device_name",
            help="Name of the broadlink device any actions should run on",
        )
        parser.add_argument(
            "--broadlink_action",
            action="append",
            help="IR action to activate with this state",
        )

    def run(self, args: argparse.Namespace):
        # Validate
        if not args.icon in ICON_NAMES:
            print(
                f"Invalid icon '{args.icon}', valid options are {','.join(ICON_NAMES)}"
            )

        database_client = APIDatabaseClient()
        aircon_manager = ACManager()

        # Save AC state if requested
        ac_state_id = None
        if args.ac_device_name:
            ac_state_id = save_state(
                database_client,
                args.name,
                aircon_manager.get_device(args.ac_device_name),
            )

        # Find the scene ID if requested
        hue_scene_id = None
        if args.hue_scene_name:
            hue_manager = HueManager()
            hue_bridge: HueBridge = hue_manager.get_bridge("Home")
            with hue_bridge.start_session() as conn:
                rooms = conn.room.get_rooms()
                scenes = conn.scene.get_scenes()
            # Select room with the right name
            selected_room = None
            for room in rooms:
                if room.name == args.room_name:
                    selected_room = room
                    break
            if not selected_room:
                print(f"Failed to find the hue room with name '{args.room_name}'")
                raise SystemExit(1)
            # Now try and find the scene
            selected_scene = None
            for scene in scenes:
                if (
                    scene.room == selected_room.identifier
                    and scene.name == args.hue_scene_name
                ):
                    selected_scene = scene
                    break
            if not selected_room:
                print(f"Failed to find the hue scene with name '{args.hue_scene_name}'")
                raise SystemExit(1)
            hue_scene_id = selected_scene.identifier

        room_state = RoomState(
            state_id=str(uuid4()),
            name=args.name,
            room_name=args.room_name,
            icon=args.icon,
            ac_device_name=args.ac_device_name,
            ac_state_id=ac_state_id,
            hue_scene_id=hue_scene_id,
            broadlink_device_name=args.broadlink_device_name,
            broadlink_actions=args.broadlink_action,
        )
        with database_client.connect() as conn:
            conn.rooms.add_state(room_state)

        print("Added the state")


class Command_Add(Command):
    def __init__(self) -> None:
        super().__init__(name="add", help_str="Add something to homecontrol")

    def add_arguments(self, parser):
        add_subcommands(parser, [Command_Add_User(), Command_Add_RoomState()])

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
