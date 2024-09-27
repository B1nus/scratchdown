import os
import requests

def bulk_download(project_ids, folder, xtoken):
    try:
        os.makedirs(folder, exist_ok=False)
    except Exception:
        raise Exception

    for project_id in project_ids:
        # Get token and filename for project
        token = project_token(project_id, xtoken)
        filename = os.path.join(folder, str(project_id))# + ".sb3")

        print("Downloading " + filename + "...")
        download(project_id, filename, token)

def download(project_id, filename, token):
    try:
        if filename is None:
            filename = str(project_id) # + ".sb3"
        response = requests.get(
            "https://projects.scratch.mit.edu/{" + str(project_id) + "}?token=" + token,
            timeout=10
        )
        open(filename + ".sb3", "wb").write(response.content)

    except Exception:
        raise("Could not download project id: " + str(project_id) + " destination: " + filename)

def project_token(project_id, xtoken):
    response = requests.get(
        "https://api.scratch.mit.edu/projects/" + str(project_id),
        headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
            "x-token": xtoken,
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        },
        timeout=10,
    )
    if "429" in str(response) or "Too many requests" == response.text:
        return None
    else:
        return response.json()["project_token"]
