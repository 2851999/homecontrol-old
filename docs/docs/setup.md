# Website Setup on Raspberry Pi

To setup [`homecontrol`](https://github.com/2851999/homecontrol) and [`homecontrol-ui`](https://github.com/2851999/homecontrol-ui) together
on a linux machine follow the below steps.

## Building `homecontrol-ui`
First we will build the website from source. To do this first ensure you have node.js e.g. by
following [this](https://learn.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-wsl).

Now install yarn with

```bash
npm install yarn
```

Clone the source with

```bash
git clone https://github.com/2851999/homecontrol-ui.git
```

Then navigate into the directory and install the dependencies

```bash
cd ./homecontrol-ui
yarn install
```

Then build the site with

```bash
yarn build
```

This will build the site producing a folder `/build` containing the built site.


## Installing dependencies on RaspberryPi
```bash
sudo apt-get update
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi-py3
sudo apt-get install sqlite3
sudo apt-get install mariadb-server
```

## Setting up the database

Now secure the database using
```bash
sudo systemctl start mysql
sudo mysql_secure_installation
```

!!! note
        You may need to use `sudo service mysql start` if you are using WSL.

Now you may login using
```bash
sudo mysql -u root -p
```

You can test the connection works using `telnet localhost 3306`.

Now create the database and user for homecontrol using
```sql
create database homecontrol;
grant all privileges on homecontrol.* TO 'INSERT_USERNAME'@'localhost' identified by 'INSERT_PASSWORD';
flush privileges;
```

## Installing `homecontrol`
```bash
git clone https://github.com/2851999/homecontrol.git

cd ./homecontrol
pip install .
```

## Copying the built website

Copy the the built site files to `/var/www/html` so they can be served by Apache.

## Adding configuration

### WSGI

Create a file `/var/www/homecontrol/api.wsgi` with the following contents

```python
import sys
sys.path.insert(0, '/var/www/homecontrol')
from homecontrol.api.main import app as application
```

### Apache
```apacheconf
Listen 5000
WSGIPythonPath /usr/local/lib/python3.9/dist-packages/
<VirtualHost *:5000>
        WSGIDaemonProcess homecontrol user=www-data group=www-data threads=2
        WSGIScriptAlias / /var/www/homecontrol/api.wsgi
        <Directory "/var/www/homecontrol">
                WSGIProcessGroup homecontrol
                WSGIScriptReloading On
                WSGIApplicationGroup %{GLOBAL}
                Require all granted
        </Directory>
        ErrorLog /var/log/homecontrol/error.log
</VirtualHost>
<VirtualHost *:80>
        <Directory "/var/www/html">
                Require all granted
        </Directory>
</VirtualHost>
```

### `homecontrol`

'homecontrol' requires several config files to function. Examples are found in the source for

- `aircon.json`
- `hue.json`
- `api.json`
- `client.json`
- `scheduler.json`
- `database.json`

These should be placed into a folder at `/etc/homecontrol`.

## Starting the site

Enable the site and restart apache

```bash
sudo /usr/sbin/a2ensite homecontrol.conf
sudo systemctl restart apache2
```

!!! warning
    WSGIPythonPath should point to your python path
!!! warning
    You may need to create the log directory manually in order to get the site to start
    ```bash
    sudo mkdir /var/log/homecontrol
    ```

## Setup the scheduler

For monitoring, setup the scheduler as a systemd service. This can be done by creating a
file at `/etc/systemd/system/homecontrol-scheduler.service` with the following contents

```ini
[Unit]
Description=homecontrol-scheduler
After=network.target

[Service]
User=www-data
Group=www-data
Type=simple
Restart=always
ExecStartPre=homecontrol-scheduler init-db
ExecStart=homecontrol-scheduler

[Install]
WantedBy=multi-user.target
```

!!! note
    The `database.path` parameter in `scheduler.json` must exist and the folder that will
    contain the database must have permissions for the users that `homecontrol-scheduler`
    and `homecontrol.api` runs with.

    This can be achieved using

    ```bash
    sudo chown -R www-data:www-data <folder>
    ```

Now reload the daemon and enable/start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable homecontrol-scheduler.service
sudo systemctl start homecontrol-scheduler
```