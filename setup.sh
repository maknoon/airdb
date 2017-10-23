!/bin/bash

echo "Setting up system..."
sudo apt-get update
echo "Updating..."
sudo apt-get install apache2
echo "Installed apache2."
sudo apt-get install libapache2-mod-wsgi
echo "Installed wsgi module for apache2."
sudo apt-get install mysql-server
echo "Installed mySQL-server."
sudo apt-get install libmysqlclient-dev
echo "Installed libmysqlclient-dev"

sudo apt-get install python-pip
echo "Installed pip."
sudo apt-get install python-dev
echo "Installed python-dev."
sudo pip install flask
echo "Installed flask."
sudo pip install MySQL-python
echo "Installed MySQL-python."

AIRDB='airdb'
mkdir ~/$AIRDB
echo "Made directory $AIRDB"
sudo ln -sT ~/$AIRDB /var/www/html/$AIRDB
echo "Linked dir $AIRDB to /var/www/html."
echo "Setup complete!"

