import requests
import os
import json
import copy
import argparse

#TODO: Add error handling for missing env vars
tfe_user_token = os.environ['TFE_USER_TOKEN']
tfe_org = os.environ['TFE_ORG']
tfe_url = os.environ['TFE_URL']

headers={
    "Authorization": f"Bearer {tfe_user_token}",
    "Content-Type": "application/vnd.api+json",
}

#TODO: add arg parsing
# def arg_parse():
#     parser = argparse.ArgumentParser(description='TFE Variable Set Copy')
#     parser.add_argument('--org', '-o', type=str, help='TFE Organization', required=True)
#     parser.add_argument('--url', '-u', type=str, help='TFE URL', required=True)
#     parser.add_argument('--token', '-t', type=str, help='TFE User Token', required=True)
#     args = parser.parse_args()
#     return args


# get all a list of variable sets for a single
def get_varsets():
    try:
        response = requests.get(
            url=f"https://{tfe_url}/api/v2/organizations/{tfe_org}/varsets",
            headers=headers,
        )
        if response.status_code == 200:
            varsets_data = response.json()  # Convert the response to JSON
            # with open(f"tfe-var-sets-{tfe_org}.json", "w") as file:
            #     json.dump(varsets_data, file)
            return varsets_data 
            
        else:  # Handle error responses
            print('Error:', response.status_code)
            print('Response HTTP Response Body:', response.content.decode())
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed:', str(e))
        #TODO: add pagination


def get_variables(varset_id):
    try:
        response = requests.get(
            url=f"https://{tfe_url}/api/v2/varsets/{varset_id}/relationships/vars",
            headers=headers,
        )
        if response.status_code == 200:
            variables_data = response.json()  # Convert the response to JSON
            # with open(f"tfe-var-{tfe_org}-{varset_id}-variables.json", "w") as file:
            #     json.dump(variables_data, file)
            return variables_data
        else:  # Handle error responses
            print('Error:', response.status_code)
            print('Response HTTP Response Body:', response.content.decode())
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed:', str(e))
                #TODO: add pagination



def get_variable(var_id):
    try:
        response = requests.get(
            url=f"https://{tfe_url}/api/v2/vars/{var_id}",
            headers=headers,
        )
        if response.status_code == 200:
            variable_data = response.json()  # Convert the response to JSON
            # with open(f"tfe-var-{tfe_org}-{var_id}.json", "w") as file:
            #     json.dump(variable_data, file)
            return variable_data
        else:  # Handle error responses
            print('Error:', response.status_code)
            print('Response HTTP Response Body:', response.content.decode())
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed:', str(e))


def get_all_workspaces():
    try:
        response = requests.get(
            url=f"https://{tfe_url}/api/v2/organizations/{tfe_org}/workspaces",
            headers=headers,
        )
        if response.status_code == 200:
            all_workspaces_data = response.json()  # Convert the response to JSON
            # with open(f"tfe-workspaces-{tfe_org}.json", "w") as file:
            #     json.dump(all_workspaces_data, file)
            return all_workspaces_data
        else:  # Handle error responses
            print('Error:', response.status_code)
            print('Response HTTP Response Body:', response.content.decode())
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed:', str(e))
                #TODO: add pagination



def get_workspace(workspace_id):
    try:
        response = requests.get(
            url=f"https://{tfe_url}/api/v2/workspaces/{workspace_id}",
            headers=headers,
        )
        if response.status_code == 200:
            workspace_data = response.json()  # Convert the response to JSON
            # with open(f"tfe-workspace-{tfe_org}-{workspace_id}.json", "w") as file:
            #     json.dump(workspace_data, file)
            return workspace_data
        else:  # Handle error responses
            print('Error:', response.status_code)
            print('Response HTTP Response Body:', response.content.decode())
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed:', str(e))


def get_project(project_id):
    try:
        response = requests.get(
            url=f"https://{tfe_url}/api/v2/projects/{project_id}",
            headers=headers,
        )
        if response.status_code == 200:
            project_data = response.json()  # Convert the response to JSON
            # with open(f"tfe-project-{tfe_org}-{project_id}.json", "w") as file:
            #     json.dump(project_data, file)
            print(f"get_project for {project_id} complete")
            return project_data
        else:  # Handle error responses
            print('Error:', response.status_code)
            print('Response HTTP Response Body:', response.content.decode())
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed:', str(e))

def get_varset(varset_id):
    try:
        response = requests.get(
            url=f"https://{tfe_url}/api/v2/varsets/{varset_id}",
            headers=headers,
        )
        if response.status_code == 200:
            varset_data = response.json()  # Convert the response to JSON
            # with open(f"tfe-var-{tfe_org}-{varset_id}.json", "w") as file:
            #     json.dump(varset_data, file)
            return varset_data
        else:  # Handle error responses
            print('Error:', response.status_code)
            print('Response HTTP Response Body:', response.content.decode())
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed:', str(e))


def post_variable(payload):
    try:
        response = requests.post(
            url=f"https://{tfe_url}/api/v2/vars",
            headers=headers,
            data=json.dumps(payload),
        )
        if response.status_code == 201:
            new_variable_data = response.json()  # Convert the response to JSON
            with open(f"tfe-var-{tfe_org}-{payload['data']['attributes']['key']} - {payload['data']['relationships']['workspace']['data']['id']}.json", "w") as file:
                json.dump(new_variable_data, file)
            print(f"new variable {payload['data']['attributes']['key']} created in {payload['data']['relationships']['workspace']['data']['id']}")
            return new_variable_data
        else:  # Handle error responses
            print('Error:', response.status_code)
            print(f"{url} Response Body:", response.content.decode())
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed:', str(e))


def get_workspace_list(varset_id):
    varset_data = get_varset(varset_id)
    workspace_list = []
    if varset_data["data"]["attributes"]["global"] == True:
        for workspace in all_workspaces_data["data"]:
            workspace_list.append(workspace["id"]) if workspace["id"] not in workspace_list else workspace_list
        # print(f"{varset_id} is global, all workspaces: {workspace_list}")
        return workspace_list
    else:
        if varset_data["data"]["attributes"]["project-count"] > 0:
            project_list = []
            if 'projects' in varset_data["data"]["relationships"]:
                for project in varset_data["data"]["relationships"]["projects"]["data"]:
                    project_list.append(project["id"])
            for project in project_list:
                for workspace in all_workspaces_data["data"]:
                    if workspace["relationships"]["project"]["data"]["id"] == project:
                        workspace_list.append(workspace["id"]) if workspace["id"] not in workspace_list else workspace_list                    
        if varset_data["data"]["attributes"]["workspace-count"] > 0:
            if 'workspaces' in varset_data["data"]["relationships"]:
                for workspace in varset_data["data"]["relationships"]["workspaces"]["data"]:
                    workspace_list.append(workspace["id"]) if workspace["id"] not in workspace_list else workspace_list
    # if workspace_list == []:
    #     print(f"{varset_id} has no workspaces")
    # else:
    #     print(f"{varset_id} workspaces: {workspace_list}")
    return workspace_list
            

def check_variable_exists(key,workspace):
    workspace_data = get_workspace(workspace)

    var_list = []
    key_list = []
    
    if 'vars' in workspace_data["data"]["relationships"]:
        for var in workspace_data["data"]["relationships"]["vars"]["data"]:
            var_list.append(var["id"])
    else:
        return False
    
    for var_id in var_list:
        existing_var = get_variable(var_id)
        key_list.append(existing_var["data"]["attributes"]["key"])

    if key in key_list:
        return True
    else:
        return False
    

def write_payload(key,value,description,category,hcl,sensitive,workspace,varset_id):
    # the template json holds the basic info
    with open('tfe-new-variable.json') as file:
        json_template = json.load(file)

    # copy the template json and build the new json on top of it
    payload_json = copy.deepcopy(json_template)
    payload_json["data"]["attributes"]["key"] = key
    payload_json["data"]["attributes"]["value"] = value
    payload_json["data"]["attributes"]["description"] = f"{description} - copied from {varset_id}"
    payload_json["data"]["attributes"]["category"] = category
    payload_json["data"]["attributes"]['hcl'] = hcl
    payload_json["data"]["attributes"]['sensitive'] = sensitive
    payload_json["data"]["relationships"]["workspace"]["data"]["id"] = workspace
    with open(f"tfe-new-variable-{tfe_org}-{key}-{workspace}.json", "w") as file:
        json.dump(payload_json, file)
    post_variable(payload_json)


# def main():

varsets_data = get_varsets()
all_workspaces_data = get_all_workspaces()

for varset in varsets_data["data"]:
    variables_data = get_variables(varset["id"])
    workspace_list = get_workspace_list(varset["id"])
    for var in variables_data["data"]:
        key = var["attributes"]['key']
        value = var["attributes"]['value']
        description = var["attributes"]['description']
        category = var["attributes"]['category']
        hcl = var["attributes"]['hcl']
        sensitive = var["attributes"]['sensitive']
        for workspace in workspace_list:
            if check_variable_exists(key,workspace) == False:
                print(f"{key} will be added to {workspace}")
                write_payload(key,value,description,category,hcl,sensitive,workspace,varset["id"])
            else:
                print(f"{key} exists in {workspace}")

# main()