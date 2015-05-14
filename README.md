52.25.22.130:80
user: grader
password: a3D@bc

This app is already [registered with google] (https://console.developers.google.com) 
[and facebook] (https://developers.facebook.com/).

Beyond a standard Python 2.7.x installation you will need to install the following:

    $ sudo apt-get install python-pip
    $ sudo pip install flask
    $ sudo pip install sqlalchemy
    $ sudo pip install requests
    $ sudo pip install httplib2
    $ sudo pip install oauth2client

To run the server:

    $ python database_setup.py #to setup the database if needed
    $ python Project5.py #to run the server

point your browser to http://52.25.22.130/catalog/

