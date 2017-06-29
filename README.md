# WASaaS Automation
Automate the configuration and management of WebSphere Application Server as a Service

This repository is part of the [Java EE Modernization Reference Implementation](https://github.com/ibm-cloud-architecture/refarch-jee)


## Create a UrbanCode Deploy Execution Proxy
The purpose of the execution proxy is to create an environment that has network access to both the UCD Server and the Bluemix environment, as well as all the tools and utilities necessary to manage the environment.
To achieve this we create a virtual machine based on RHEL 7 and install the relevant prerequisites

### Configuration steps
1. Install prerequisites

    ```
    $ sudo rpm -i https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
    $ sudo yum clean all
    $ sudo yum install java ansible git python-pip
    $ sudo pip install requests
    ```

1. Download the UCD Agent from the UCD Server and install

    ```
    $ wget https://<ucd_server>/tools/ibm-ucd-agent.zip
    $ unzip ibm-ucd-agent.zip
    $ cd ibm-ucd-agent 
    $ sudo ./install-agent.sh
    ```
    Follow the installation instructions

1. Configure the UCD agent to start at boot time
   
   ```
   $ sudo cp /opt/urbancode/ibm-ucdagent/bin/agent /etc/init.d/ibm-ucdagent
   $ sudo sed -i 's/AGENT_GROUP=/AGENT_GROUP=root/g' /etc/init.d/ibm-ucdagent
   $ sudo sed -i 's/AGENT_USER=/AGENT_USER=root/g' /etc/init.d/ibm-ucdagent
   $ sudo chkconfig --add ibm-ucdagent
   $ sudo service ibm-ucdagent start
   ```

1. Setup the WASaaS OpenVPN file for your region

   This step is ripe for automation, but right now, just do it manually

1. Create the UCD virtual user

   ```
   $ sudo adduser virtuser
   ```
   
1. Clone the script repository into the virtuser

   ```
   $ sudo su - virtuser
   $ git clone https://github.com/hassenius/wasaas-setup.git
   ```

1. Create necessary ssh key files (as virtuser)

    ```
    $ ssh_keygen
    ```
    
    make sure to save the key to the default location ```/home/virtuser/.ssh/id_rsa``` and use ***no passphrase***


