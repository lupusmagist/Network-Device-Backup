# Network Device Backup App

*The well chosen and descriptive name above basically says it all.*

This is a Python/Flask/Netmiko/Paramiko/Docker/Nginx/PostgreSQL app that provides a UI for backing up of network devices via ssh.

Commands are issued to the device to create a text export and this export is saved to the database in a encrypted form.

For that app to run Docker and Docker-Compose has to be installed on the host.
Configuration for Docker is via docker-compose.yml.
Default settings will start app in stand-alone mode.

If you have a existing web server that you would like to use, disable the Nginx section in the docker-compose.yml and use the nginx.conf in the websrv folder as template to configure your web server.

If you have a existing database server that you would like to use, disable the database section in the docker-compose.yml and configure the app by changing the SQLALCHEMY_DATABASE_URI under the ProductionConfig class in the settings.py file

### Starting the app in default mode.

* Ensure that Docker and Docker-Compose is installed.
* Create a folder for the app and in that folder do:
    * git clone https://github.com/lupusmagist/Network-Device-Backup.git
* cd into the app folder
* create a new .env file and copy the contents below into the file. (You can change any of the variables)
```
COMPOSE_PROJECT_NAME=Device_Backup
POSTGRES_USER=dbuser
POSTGRES_PASSWORD=dbpassword
POSTGRES_DB=DM
```
* run 'docker-compose up'

In your web browser of choice connect to: http://your-host-ip

