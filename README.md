# Dependabot_Alerts

## Overview
Dependabot performs a scan to detect vulnerable dependencies and sends Dependabot alerts when:

* A new vulnerability is added to the GitHub Advisory Database . 

* The dependency graph for a repository changes. For example, when a contributor pushes a commit to change the packages or versions it depends on, or when the code of one of the dependencies changes.

## Usage

#### Editing the configuration file (conf/config.toml):
 - Update the platform field as necessary.  
 - Add your CSV Filename that is being created as an artifact.  
 - Provide the network name of the upload to be done, the script will fetch the network ID.
 - Input the Client ID of the Risksense Account. 

```toml
platform_url = 'https://platform-in.risksense.com'

# Specify the path to the folder containing the files you wish to upload.
# If you update this, please use the absolute path to your desired folder.
csv_filename = ''
folder = ''

# Trigger URBA upon completion of upload processing.
#auto_urba = true

# You may uncomment this parameter and enter the desired network ID for your upload here if you already know it.
#network_id = 155014
network_name = '' # Enter the desired Network Name

# You may uncomment this parameter and enter the desired client ID for your upload here if you already know it.
client_id = '' # Enter the desired Client ID
```


#### Running Dependabot.yml Workflow:

After configuring the conf.toml, any changes detected in the repository will trigger the workflow.

The Dependabot.yml workflow will pull the alerts produced by Dependabot from the repo mentioned in the **Secrets** and produce the data into a CSV file.

The CSV file will be uplaoed into Risksense.

#### Updating the Secrets:

##### Update the secrets as mentioned below 

AUTH_TOKEN1 - GitHub API key of the target Repo

OWNER - Owner name of the Target

OWNER_REPO - "Owner name of the Traget" *(In Quotes)

REPO - "Repo name of the Target" *(In Quotes)

REPO_NAME - Repo name of the Target

RS_API_KEY - API Key of RiskSense 
