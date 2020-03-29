#!/usr/bin/env python3

import argparse
import csv
import json
import math
import requests
import sys

GITHUB_API_URL = "https://api.github.com"

parser = argparse.ArgumentParser(description='Usage: stargazers')
parser.add_argument("--owner", type=str, help="github username of repository owner")
parser.add_argument("--repo", type=str, help="github repository name")
parser.add_argument("-u", "--username", type=str, help="your github username")
parser.add_argument("-t", "--token", type=str, help="your github token. to create new token, go to https://github.com/settings/tokens")
parser.add_argument("--output-type", type=str, choices=["csv", "json"], help="output type as either csv or json")
parser.add_argument("-o", "--out-file", type=str, default="stargazers", help="name of the output file (default: stargazers)")

args = parser.parse_args()
print(args)
output_type = args.output_type
out_file = args.out_file

def get_stargazers_count(owner, repo):
    response = get_request("{0}/repos/{1}/{2}".format(GITHUB_API_URL, owner, repo))
    return response["stargazers_count"]
    
def get_request(url, auth=None, headers=None, params=None):
    response = requests.get(url, auth=auth, headers=headers, params=params)
    response_json = response.json()
    if response.status_code != 200:
        print("Non-200 status code received: {0}".format(response_json["message"]))
        print("Ensure that the passed parameters are valid and try again.")
        sys.exit(1)
    return response_json

def get_stargazers(owner, repo, username, token):
    total_stars = get_stargazers_count(owner, repo)
    total_requests = math.ceil(total_stars / 30)
    auth = (username, token)
    headers = { "Accept": "application/vnd.github.v3+json" }
    if output_type == "json":
        out_json=[]
    if output_type == "csv":
        csv_writer = csv.writer(open("{0}.csv".format(out_file), "w"))
        csv_writer.writerow([
            "login",
            "id",
            "node_id",
            "avatar_url",
            "gravatar_id",
            "url","html_url",
            "followers_url",
            "following_url",
            "gists_url",
            "starred_url",
            "subscriptions_url",
            "organizations_url",
            "repos_url","events_url",
            "received_events_url",
            "type",
            "site_admin"
        ])
    for i in range(1, total_requests+1):
        response = get_request(
            "{0}/repos/{1}/{2}/stargazers".format(GITHUB_API_URL, owner, repo),
            auth=auth,
            headers=headers,
            params={ "page": str(i) }
        )
        for user in response:
            if output_type == "json":
                out_json.append(user)
            elif output_type == "csv":
                csv_writer.writerow([
                    user["login"],
                    user["login"],
                    user["id"],
                    user["node_id"],
                    user["avatar_url"],
                    user["gravatar_id"],
                    user["url"],
                    user["html_url"],
                    user["followers_url"],
                    user["following_url"],
                    user["gists_url"],
                    user["starred_url"],
                    user["subscriptions_url"],
                    user["organizations_url"],
                    user["repos_url"],
                    user["events_url"],
                    user["received_events_url"],
                    user["type"],
                    user["site_admin"]
                ])
    if output_type == "json":
        with open(out_file, 'w') as outfile:
            json.dump(out_json, outfile)
    elif output_type != "csv":
        print(out_json)
    print("{0} DONE {0}".format("*"*5))

if __name__ == "__main__":
    get_stargazers(args.owner, args.repo, args.username, args.token)

