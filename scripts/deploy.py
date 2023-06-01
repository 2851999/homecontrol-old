from pathlib import Path
import subprocess

# Values specific to my setup
DEPLOY_USER = "joel"
DEPLOY_DOMAIN = "homecontrol"

LOCAL_HOMECONTROL_DIR = Path("~/homecontrol").expanduser()
LOCAL_HOMECONTROL_UI_DIR = Path("~/homecontrol-ui").expanduser()

DEPLOY_HOMECONTROL_DIR = "~/homecontrol"
DEPLOY_HOMECONTROL_UI_BUILD_TEMP_DIR = "~/homecontrol-ui-build"
DEPLOY_HOMECONTROL_UI_DIR = "/var/www/html/"

DEPLOY_HOMECONTROL_CONFIG_FILES = [
    "aircon.json",
    # "hue.json", # Don't always do this as changes path to cert
    "api.json",
    "client.json",
    "scheduler.json",
    "database.json",
    "broadlink.json",
]

VERBOSE = False


def get_ssh_dest():
    return f"{DEPLOY_USER}@{DEPLOY_DOMAIN}"


def run_command(command, cwd=None):
    # Allow multiple commands
    if isinstance(command, list):
        command = ";".join(command)
    if VERBOSE:
        subprocess.Popen(command, shell=True, cwd=cwd).wait()
    else:
        subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        ).wait()


def run_ssh_command(command):
    # Allow multiple commands
    if isinstance(command, list):
        command = ";".join(command)
    ssh_process = subprocess.Popen(
        ["ssh", get_ssh_dest(), command],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    if VERBOSE:
        for stdout_line in iter(ssh_process.stdout.readline, ""):
            print(stdout_line.replace("\n", ""))
        ssh_process.stdout.close()
    return_code = ssh_process.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, command)


def copy_folder(src, dest):
    run_command(f"scp -r {src} {get_ssh_dest()}:{dest}")


def build_and_deploy():
    # Build ui
    print("Building homecontrol-ui...")
    run_command("yarn build", LOCAL_HOMECONTROL_UI_DIR)

    # Disable scheduler (uninstalling gives permission denied otherwise)
    print("Disabling homecontrol-scheduler...")
    run_ssh_command(
        [
            "sudo systemctl stop homecontrol-scheduler",
            "sudo systemctl disable homecontrol-scheduler",
        ]
    )

    # Remove existing installation
    print("Removing existing installation...")
    run_ssh_command(
        [
            "sudo pip uninstall -y homecontrol",
            "sudo rm -rf homecontrol",
            "rm -rf homecontrol-ui-build/*",
        ]
    )

    # Copy new versions
    print("Copying new versions...")
    copy_folder(LOCAL_HOMECONTROL_DIR, DEPLOY_HOMECONTROL_DIR)
    copy_folder(
        f"{LOCAL_HOMECONTROL_UI_DIR}/build/*", DEPLOY_HOMECONTROL_UI_BUILD_TEMP_DIR
    )

    # Remove old site
    print("Removing old site...")
    run_ssh_command(f"sudo rm -rf {DEPLOY_HOMECONTROL_UI_DIR}/*")

    # Copy new site
    print("Copying new site...")
    run_ssh_command(
        f"sudo mv -f {DEPLOY_HOMECONTROL_UI_BUILD_TEMP_DIR}/* {DEPLOY_HOMECONTROL_UI_DIR}"
    )

    # Install homecontrol
    print("Installing homecontrol...")
    run_ssh_command(f"sudo pip install -r {DEPLOY_HOMECONTROL_DIR}/requirements.txt")
    run_ssh_command(f"sudo pip install {DEPLOY_HOMECONTROL_DIR}")

    # Copying new config
    print("Updating config...")
    run_ssh_command(
        [
            f"sudo cp {DEPLOY_HOMECONTROL_DIR}/{file} /etc/homecontrol/{file}"
            for file in DEPLOY_HOMECONTROL_CONFIG_FILES
        ]
    )

    # Restart apache service
    print("Restarting apache...")
    run_ssh_command("sudo systemctl restart apache2")

    # Restart scheduler
    print("Enabling homecontrol-scheduler...")
    run_ssh_command("sudo systemctl enable homecontrol-scheduler")
    run_ssh_command("sudo systemctl start homecontrol-scheduler")


if __name__ == "__main__":
    build_and_deploy()
