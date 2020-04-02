# Network Device Backup App

*The well chosen and descriptive name above basicly says it all.*

This is a Python/Flask/Netmiko/Paramiko/Docker/nginx/PostgreSQL app that provides a UI for backing up of network devices via ssh.

Commands are issued to the device to create a text export and this export is saved to the database in a encryted form.

For that app to run Docker and Docker-Compose has to be installed on the host.
Configuration for Docker is via docker-compose.yml.
Default settings will start app in stand-alone mode.

If you have a existing web server that you would like to use, disable the Nginx section in the docker-compose.yml and use the nginx.conf in the websrv folder as template to configure your web server.

If you have a exsiting database server that you would like to use, disable the database section in the docker-compose.yml and configure the app by changing the SQLALCHEMY_DATABASE_URI under the ProductionConfig class in the settings.py file

### Starting the app in default mode.

Ensure that Docker and Docker-Compose is installed.


gunicorn -b 0.0.0.0:8000 --log-file=- -e FLASK_DEBUG=development  --worker-tmp-dir /dev/shm "webapp:create_app()"
