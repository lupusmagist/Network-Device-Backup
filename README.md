# Network Device Backup App

*The well chosen and descriptive name above basically says it all.*

This is a Python/Flask/Netmiko/Paramiko/Docker/Nginx/RabbitMQ/PostgreSQL app that provides a UI for backing up of network devices via ssh.

Commands are issued to the device to create a text export and this export is saved to the database.

For that app to run Docker and Docker-Compose has to be installed on the host.
Configuration for Docker is via docker-compose.yml.
Default settings will start app in defualt Docker mode.

If you have a existing web server that you would like to use, disable the Nginx section in the docker-compose.yml and use the nginx.conf in the websrv folder as template to configure your web server.

If you have a existing database server that you would like to use, disable the database section in the docker-compose.yml and configure the app by changing the SQLALCHEMY_DATABASE_URI under the ProductionConfig class in the settings.py file

Setting DEBUG=True in the .env file(created below) will swith the database to SQLite.

The schedule for doing backups and sending admin mails can be changed with the CELERYBEAT_SCHEDULE setting in the settings.py file. More info here: http://docs.celeryproject.org/en/master/userguide/periodic-tasks.html


### Starting the app in default mode.

* Ensure that Docker and Docker-Compose is installed.
* git clone https://github.com/lupusmagist/Network-Device-Backup.git
* cd into the app folder
* create a new .env file and copy the contents below into the file.

```
COMPOSE_PROJECT_NAME=Device_Backup
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postpass
POSTGRES_DB=DM
MAIL_USERNAME=devbackup@somewhere.com
MAIL_PASSWORD=password to send mail
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=pass
SECRET_KEY=somekey
DEBUG=False
```

* run - docker-compose build
* run - docker-compose up

* In your web browser of choice connect to: http://your-host-ip
* Default username: admin@example.com
* Default password: password

### Running as a standalone app.
Python 3.6+, PIP must be installed on the host.

A virtual enviroment is recommened unless the server will be a virtual machine for just this prupose.

* Follow the instructions as above, just without the Docker commands.
* Install RabbitMQ server on your host and ensure that it is running.
* Adjust the settings.py file to reflect the your database settings.. or
just copy the Debug database string to the production settings, the app will then use SQLite as the database, no extra depenencies needed.

* Switch to your virtual enviroment in the main app folder.
* run - pip install -r webapp/requirements.txt
* run - celery -A webapp.celery_app worker --loglevel=INFO --detach --pidfile=''
* run - celery -A webapp.celery_app beat --loglevel=INFO --detach --pidfile=''
* run - gunicorn -b 0.0.0.0:8000 --log-file=-  --worker-tmp-dir /dev/shm "webapp:create_app()"

If everthing went well you will now be able to connect to the app on http://your-host-ip

Common problems:
* When running the first celery commend, it wont be found.
    *requirements.txt was not installed*
* SQL type errors.
    *The database string in the settings.py file is not correct.*
* App is not doing backups or sending mails on schedule
    *RabbitMQ server is not running, or port in settings.py file is incorrect.*
