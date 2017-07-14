# Using the automation components

Generally the necessary variables are populated by UCD, and the python and ansible scripts are executed by the UCD Agent.
However, it is possible to populate and launch the scripts by hand. This document describes how to use the scripts.


## Setup OpenVPN
Before you can communicate with the WASaaS instance for admin purposes you must setup OpenVPN.

## Getting Bluemix API Key
The scripts make use of Bluemix API keys rather than username/password combination to communicate with the Bluemix APIs.
To get and manage API keys on your Bluemix account follow the instructions in [Bluemix docs](https://console.bluemix.net/docs/iam/apikeys.html#manapikey)

## Configuring WAS instance
This step configures the new WebSphere instance using jython; creating the necessary users, groups and sets up JDBC to run the CustomerOrder application

1. Populate the vars.yaml file

    example vars.yaml:

    ```
    organisation: cent@us.ibm.com
    space: pc-stonehenge-dev
    apiKey: <secret key here>
    regionKey: ng
    instanceName: hkm-wasaas-inf-dev
    install: ['was_profile']
    ```


1. Populate ansible/was-vars.yaml
    example:

    ```
    dbuser: db2inst1
    dbpass: <top secret password>
    dbhost: cap-sg-prd-2.integration.ibmcloud.com
    dbport: 16516
    ```

1. Run ```python manageWASaaS.py```

## Installing UCD Agent
This step installs the UCD Agent on the new instance. You can specify rules in UCD to automatically add the new agent to a top level resource based on naming convention.
In the example below the new WAS environment is added to the WASaaS-dev environment, since the agent names contains integration.wasaas.stonehenge.case.com which matches the relevant auto-add rule in UCD.

1. populate the vars.yaml file

    example vars.yaml:

    ```
    organisation: cent@us.ibm.com
    space: pc-stonehenge-dev
    apiKey: <secret key here>
    regionKey: ng
    instanceName: hkm-wasaas-inf-dev
    install: ['ucdagent']
    ```

1. populate ansible/ucd-vars.yaml

    example ansible/ucd-vars.yaml:

    ```
    ucd_server_url: https://ucdeploy2.swg-devops.com
    ucd_host: ucdeploy2.swg-devops.com
    ucd_port: 7918
    ucd_teams: Cloud Architecture Solution Engineering
    ucd_agent_name: dev7.integration.wasaas.stonehenge.case.com
    ```

1. Run ```python manageWASaaS.py```


## Configure UCD and WAS in the same run

1. Populate ```ansible/was-vars.yaml```, ```ansible/ucd-vars.yaml``` and ```vars.yaml``` as described above, but include both install directives in ```vars.yaml```:
    
    example vars.yaml:

    ```
    organisation: cent@us.ibm.com
    space: pc-stonehenge-dev
    apiKey: <secret key here>
    regionKey: ng
    instanceName: hkm-wasaas-inf-dev
    install: ['ucdagent', 'was_profile']
    ```
   
1. Run ```python manageWASaaS.py```


## Install and configure monitoring agent

Not completed yet
