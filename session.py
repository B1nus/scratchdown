import requests
import json
import re

HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        "x-csrftoken": "a",
        "x-requested-with": "XMLHttpRequest",
        "referer": "https://scratch.mit.edu",
        }
COOKIE = "scratchcsrftoken=a;scratchlanguage=en;"

# Returns session_id
def login(username, password):
    data = json.dumps({"username": username, "password": password})
    _headers = HEADERS
    _headers["Cookie"] = COOKIE
    request = requests.post(
            "https://scratch.mit.edu/login/", data=data, headers=_headers,
            timeout = 10,
            )

    try:
        # Use re to find the session_id
        session_id = str(re.search('"(.*)"', request.headers["Set-Cookie"]).group())
        return session_id
    except Exception:
        return None

# Return xtoken
def xtoken(session_id):
    try:
        response = json.loads(requests.post(
            "https://scratch.mit.edu/session",
            headers = HEADERS,
            cookies = {
                "scratchsessionsid" : session_id,
                "scratchcsrftoken" : "a",
                "scratchlanguage" : "en"
                }, timeout=10
            ).text)

        return response['user']['token']

    except Exception:
        print("Something went wrong while fetching the xtoken.")
