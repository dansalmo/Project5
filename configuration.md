To launch a new remote Virtual Machine to my Udacity account:

    Indent each line by at least 1 tab, or 4 spaces.
    var Mou = exactlyTheAppIwant; 

1. Download [this private key](https://www.udacity.com/f200d503-b6f3-415a-aeb6-a9f5d839e528)

1. Move the private key file into the folder ~/.ssh (where ~ is your environment's home directory). So if you downloaded the file to the Downloads folder, just execute the following command in your terminal

		$ mv ~/Downloads/udacity_key.rsa ~/.ssh/    

1. Open your terminal and type:

    	$ chmod 600 ~/.ssh/udacity_key.rs

1. Login to your remote VM.  In your terminal, type i

		$ ssh -i ~/.ssh/udacity_key.rsa root@52.25.22.130

1. Create a new user named grader with a secure password and give grader the permission to 'sudo'

1. Copy the RSA key to the grader user folder

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

1. Create a cron job to keep packages updated

1. Change the SSH port from 22 to 2200

    	#log back in as grader using port 2200
    	$ ssh -p 2200 -i ~/.ssh/udacity_key.rsa grader@52.25.22.130

Configure the Universal Firewall to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)

Configure the local timezone to UTC

Install and configure Apache to serve a Python mod_wsgi application

Install and configure PostgreSQL:

Do not allow remote connections

Create a new user named catalog that has limited permissions to your catalog application database

Install git, clone and setup your Catalog App project (from your GitHub repository from earlier in the Nanodegree program) so that it functions correctly when visiting your server’s IP address in a browser. Remember to set this up appropriately so that your .git directory is not publicly accessible via a browser!