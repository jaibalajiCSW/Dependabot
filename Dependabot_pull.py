import requests
import json
import csv
import os

repo_url = f'https://github.com/' + os.getenv('OWNER') + '/' + os.getenv('REPO') + '/' # Enter URL of desired repo and owner of the repo. (Secrets)
headers = {"Authorization":  os.getenv('AUTH_TOKEN1')} # Enter Github API key of the target Repo (Secrets)
severity_mapping = {'CRITICAL': 10, 'HIGH': 8.9, 'MODERATE': 6.9, 'LOW': 3.9}
def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
        
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

# Format of OWNER_REPO = " "Akashbalaji" "
# Format of Repo_name' = " "Elanco" "



# The GraphQL query ( Enter login : OWNER NAME and name : REPOSITORY NAME)
# Add 
query = """{ 
    viewer 
    {
    organization(login: """+os.getenv('OWNER_REPO')+""") { 
      id
    }
    repository(name: """+os.getenv('REPO_NAME')+""") {
      id
      name
      createdAt
      vulnerabilityAlerts(first: 100) {
        nodes {
          id
          securityVulnerability {
            package {
              ecosystem
              name
            }
            severity
            advisory 
            {
              cvss {
                score
              }
              description
              ghsaId
              summary
              origin
              publishedAt
              references {
                url
              }
              description
              updatedAt
            }
          }
          vulnerableManifestFilename
          vulnerableManifestPath
        }
      }
    }
  }
}"""
result = run_query(query) # Execute the query

with open('Dependabot_Alerts.json', 'w') as out_file: # Writing JSON data into a file.
  out_file.write(json.dumps(result))

with open("Dependabot_Alerts.json") as json_format_file: # Parsing the JSON data. 
  j = json.load(json_format_file)

#Writing JSON data in CSV
csv = open(r".\files_to_process\Dependabot.csv","w")
csvdata = "Name,Pluginid,Created At,Description,Summary,Reference Type,Solution,BaseUrl,Severity,Package Name,Application URL,File Path\n"
csvdata += j['data']['viewer']['repository']['name'] + ","
for i in j['data']['viewer']['repository']['vulnerabilityAlerts']['nodes']:
  csvdata += i['id'] + "," #REQUIRED
  csvdata += i['securityVulnerability']['advisory']['publishedAt'][0:10] + "," 
  csvdata += "\"" + i['securityVulnerability']['advisory']['description']+ "\"" + "," #REQUIRED
  csvdata += i['securityVulnerability']['advisory']['summary'] + ' in ' + i['vulnerableManifestPath'] + "," #REQUIRED
  csvdata += i['securityVulnerability']['package']['ecosystem'] + "," #REQUIRED
  csvdata += 'Listed as Recommendation under Description' + "," #REQUIRED
  csvdata += 'https://github.com' + "," #REQUIRED
  csvdata += str(severity_mapping.get(i['securityVulnerability']['severity'])) + "," #REQUIRED
  csvdata += i['securityVulnerability']['package']['name'] + "," #REQUIRED
  csvdata += repo_url + "," #REQUIRED
  csvdata += repo_url + i['vulnerableManifestPath'] + "," #REQUIRED
csv.write(csvdata)
csv.close()
print(csvdata)


