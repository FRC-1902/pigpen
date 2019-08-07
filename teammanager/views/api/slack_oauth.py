import os

import requests
from django.shortcuts import redirect


def slack_login(request):
    if request.method == "GET":
        data = request.GET
        if 'code' in data:
            resp = do_oauth(data['code'])
            print(resp)

            if resp.get("ok", False) and resp.get("team", {}).get("id", "") == "T050Q5CEN":
                token = resp['access_token']
                request.session['slack_oauth'] = token
                print("Saving Session")
                identity = get_identity(token)
                if identity and "user" in identity:
                    if "id" in identity["user"]:
                        request.session["slack_id"] = identity["user"]["id"]

    return redirect("man:index")


def do_oauth(code):
    url = "https://slack.com/api/oauth.access?client_id=5024182498.703454056853&client_secret=%s&code=%s&redirect_uri=%s" % \
          (os.getenv("SLACK_SECRET", "none"), code, "https%3A%2F%2Fpen.explodingbacon.com%2Fauth%2Fslack%2Flogin")

    return requests.get(url).json()


def get_identity(token):
    return requests.get("https://slack.com/api/users.identity?token={}".format(token)).jsn()