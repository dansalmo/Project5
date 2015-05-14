To launch a new remote Virtual Machine to my Udacity account:

1. Download the private key.

1. Move the private key file into the folder ~/.ssh (where ~ is your environment's home directory). So if you downloaded the file to the Downloads folder, just execute the following command in your terminal

        $ mv ~/Downloads/udacity_key.rsa ~/.ssh/    

1. Open your terminal and type:

        $ chmod 600 ~/.ssh/udacity_key.rs

1. Login to your remote VM.  In your terminal, type i

        $ ssh -i ~/.ssh/udacity_key.rsa root@52.25.22.130

1. Create a new user named grader with a secure password and give grader the permission to 'sudo'

        #follow the prompts, make a note of the password
        $ adduser grader
        
        #edit the sudoers file with this command
        $ sudo /usr/sbin/visudo
        
        # The user privilege specification should ook like this:
        root    ALL=(ALL:ALL) ALL 
        grader    ALL=(ALL:ALL) ALL
        
        # type :wq to quit and save from the vim editor

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

            #exit and then login as grader using port 2200
            $ exit 
            $ ssh -p 2200 -i ~/.ssh/udacity_key.rsa grader@52.25.22.130

1. Configure the Universal Firewall to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)

	    $ sudo ufw allow 2200/tcp
    	$ sudo ufw allow 80/tcp
    	$ sudo ufw allow 123/tcp

1. Configure the local timezone to UTC

		$ sudo dpkg-reconfigure tzdata
		
	* Use the arrow keys to choose the bottom option `None of the Above`
	* Press the `u` key until the `UTC` option is selected and press `Return`
	
1. Install and configure Apache to serve a Python mod_wsgi application

1. Install and configure PostgreSQL:

	* Do not allow remote connections
	* Create a new user named catalog that has limited permissions to your catalog application database

Install git, clone and setup your Catalog App project (from your GitHub repository from earlier in the Nanodegree program) so that it functions correctly when visiting your server’s IP address in a browser. Remember to set this up appropriately so that your .git directory is not publicly accessible via a browser!