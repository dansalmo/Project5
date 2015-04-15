
This app is already [registered with google] (https://console.developers.google.com) 
[and facebook] (https://developers.facebook.com/).

Beyond a standard Python 2.7.x installation you will need to install the following:

`sudo pip install flask`
`sudo pip install sqlalchemy`
`sudo pip install requests`
`sudo pip install httplib2`

If you are using vagrant type:
`vagrant up`
`vagrant ssh`
`cd /vagrant/catalog` or whatever directory the project is in

`python database_setup.py` to setup the database if needed
`python Project3.py` to run the server

#point your browser to http://localhost:5000/catalog/


