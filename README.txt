This app has been registered with google (https://console.developers.google.com) 
and facebook (https://developers.facebook.com/).

This app is meant to run on a vagrant virtual machine from Udacity.

type:
vagrant up
vagrant ssh
cd /vagrant/catalog

python database_setup.py #to setup the database if needed
python Project3.py #to run the server

point your browser to http://localhost:5000/catalog/


