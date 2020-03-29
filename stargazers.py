#!/usr/bin/env python3

import argparse
import csv
import math
import os
import requests

GITHUB_API_URL = "https://api.github.com"

parser = argparse.ArgumentParser(description='Usage: stargazers')
parser.add_argument("--owner", type=str, help="github username of repository owner")
parser.add_argument("--repo", type=str, help="github repository name")
parser.add_argument("-u", "--username", type=str, help="your github username")
parser.add_argument("-t", "--token", type=str, help="your github token. to create new token, go to https://github.com/settings/tokens")
parser.add_argument("--output-type", type=str, choices=["csv", "json"], help="output type as either csv or json")
parser.add_argument("-o", "--out-file", type=str, default="stargazers", help="name of the output file (default: stargazers)")

args = parser.parse_args()
out_type = args["output-type"]
out_file = args["output-file"]

def get_stargazers_count(owner, repo):
    response = get_request("{0}/repos/{1}/{2}".format(GITHUB_API_URL, owner, repo))
    return response["stargazers_count"]
    
def get_request(url, auth=None, headers=None, params=None):
    response = requests.get(url, auth=auth, headers=headers, params=params)
    response_json = response.json()
    if response.status_code != 200:
        print("Non-200 status code received: {0}".format(response_json["message"]))
        print("Ensure that the passed parameters are valid and try again.")
        os.exit(1)
    return response_json

def get_stargazers(owner, repo, username, token):
    total_stars = get_stargazers_count(owner, repo)
    total_requests = math.ceil(total_start / 30)
    auth = (username, token)
    headers = { "Accept" "application/vnd.github.v3+json" }
    if output_type == "json":
        out_json=[]
    if output_type == "csv":
        csv_writer = csv.writer(open("{0}.csv".format(out_file), "wb+"))
        csv_writer.writerow(["login","id","node_id","avatar_url","gravatar_id","url","html_url","followers_url","following_url","gists_url","starred_url","subscriptions_url","organizations_url","repos_url","events_url","received_events_url","type","site_admin"])
    for i in range(1, total_requests+1):
        response = get_request("{0}/repos/{1}/{2}/stargazers", auth=auth, headers=headers, params={ "page": str(i) })
        if output_type == "json":
            merge_dicts(out_json, response)
        elif output_type == "csv":
            csv_writer.writerow([response["login"], response["id"], response["node_id"], response["avatar_url"], response["gravatar_id"], response["url"], response["html_url"], response["followers_url"], response["following_url"], response["gists_url"], response["starred_url"], response["subscriptions_url"], response["organizations_url"], response["repos_url"], response["events_url"], response["received_events_url"], response["type"], response["site_admin"]])
    if output_type == "json":
        with open(output_file, 'w') as outfile:
            json.dump(data, outfile)
    elif output_type != "csv":
        print(out_json)

if __name__ == "__main__":
    print(args.owner)
    print(args.repo)
    print(args.username)
    print(args.token)
    print(args["output-type"])
    print(args["out-file"])
