To launch a new remote Virtual Machine to my Udacity account:

1. Download the private key to your own machine.

1. Move the private key file into the folder ~/.ssh (where ~ is your environment's home directory). So if you downloaded the file to the Downloads folder, just execute the following command in your terminal

        $ mv ~/Downloads/udacity_key.rsa ~/.ssh/    

1. Open your terminal and type:

        $ chmod 600 ~/.ssh/udacity_key.rsa

1. Login to your remote VM.  In your terminal, type i

        $ ssh -i ~/.ssh/udacity_key.rsa root@52.25.22.130

1. Create a new user named grader with a secure password and give grader the permission to 'sudo'

        #follow the prompts, make a note of the password
        $ adduser grader sudo
        
1. Copy the RSA key to the grader user folder and set ownership

        $ sudo cp /root/.ssh .ssh
        $ chown -R grader .ssh
        $ chgrp -R grader .ssh

1. Exit the root SSH session and confirm that you can login via SSH as grader

        #exit as root
        $ exit
        
        #log back in as grader
        $ ssh -i ~/.ssh/udacity_key.rsa grader@52.25.22.130

1. As grader, use your sudo privilege to remove the ability to login as root remotely:

    * Change the PermitRootLogin line in `/etc/ssh/sshd_config` to:

        `PermitRootLogin no`
        
        Then:

            #restart the ssh service
            $ sudo service ssh restart
        
            #exit as grader
            $ exit
        
            #confirm root is blocked
            $ ssh -i ~/.ssh/udacity_key.rsa root@52.25.22.130
            Permission denied (publickey).
        
            #log back in as grader
            $ ssh -i ~/.ssh/udacity_key.rsa grader@52.25.22.130

1. Update all currently installed packages

        $ sudo apt-get update
        $ sudo apt-get upgrade                

1. Create a cron job to keep packages updated

    * Create a file named `autoupdate` that contains the following lines:

            #!/bin/bash
            apt-get update
            apt-get upgrade -y
            apt-get autoclean

    * Move the file to the cron.weekly folder and make it executable:
    
            $ sudo mv autoupdate /etc/cron.weekly
            $ sudo chmod 755 /etc/cron.weekly/autoupdate
    
1. Change the SSH port from 22 to 2200

    * Use the nano editor to change the `sshd_config` file
    * Find the line that says: `Port 22` and change it to `Port 2200`

            $ sudo nano -c /etc/ssh/sshd_config

	* Restart the SSH daemon:
			
			$ /etc/init.d/sshd restart
	
	* You should see that it was stopped and started successfully:

			Stopping sshd:              [  OK  ]
			Starting sshd:              [  OK  ]


     * Exit and then login as grader using port 2200
 
            $ exit 
            $ ssh -p 2200 -i ~/.ssh/udacity_key.rsa grader@52.25.22.130

1. Configure the Universal Firewall to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)

	    $ sudo ufw allow 2200/tcp
    	$ sudo ufw allow 80/tcp
    	$ sudo ufw allow 123/tcp

1. Install and configure Fail2Ban

		$ sudo apt-get update
		$ sudo apt-get install fail2ban
		
	* make a copy of `jail.conf` called `jail.local` then restart
	
			$ sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
			$ sudo /etc/init.d/fail2ban restart

1. Configure the local timezone to UTC

		$ sudo dpkg-reconfigure tzdata
		
	* Use the arrow keys to choose the bottom option `None of the Above`
	* Press the `u` key until the `UTC` option is selected and press `Return`
	
1. Install the required packages for the Item Catalog web application

		$ sudo pip install flask
		$ sudo pip install sqlalchemy
		$ sudo pip install requests
		$ sudo pip install httplib2
		$ sudo pip install oauth2client

1. Install git and clone the project repo into `/var/www`

		$ sudo apt-get install git
		$ sudo cd /var/www
		$ sudo git clone https://github.com/dansalmo/Project5.git


1. Install and configure Apache to serve a Python mod_wsgi application

		$ sudo apt-get install python-pip apache2 libapache2-mod-wsgi
		$ sudo cp ~/Project5/Project5.conf /etc/apache2/sites-available
		$ sudo a2enmod wsgi 
		$ sudo a2ensite Project5
		$ sudo service apache2 restart
	
1. Install and configure PostgreSQL: 

	* Do not enable any remote connections

			$ sudo apt-get install postgresql postgresql-contrib
			$ sudo apt-get install python-psycopg2
			$ sudo apt-get install libpq-dev

	* Create a new Postgres user named catalog that has limited permissions to your catalog application database


			$ sudo su - postgres
			$ psql
			postgres=# CREATE USER catalog WITH PASSWORD 'secure password';
			postgres=# GRANT SELECT, UPDATE, INSERT ON catalog TO catalog;
			postgres=# \q
			$ exit
1. Create the catalog database and reload the server

		$ python databasesetup.py
		$ sudo service apache2 restart