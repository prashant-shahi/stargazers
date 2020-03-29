# Stargazers

A small python project to obtain CSV/JSON of stargazers of any GitHub repository.


### Usage

```sh
$ python stargazers.py --help

usage: stargazers.py [-h] [--owner OWNER] [--repo REPO] [-u USERNAME]
                     [-t TOKEN] [--output-type {csv,json}] [-o OUT_FILE]

Usage: stargazers

optional arguments:
  -h, --help            show this help message and exit
  --owner OWNER         github username of repository owner
  --repo REPO           github repository name
  -u USERNAME, --username USERNAME
                        your github username
  -t TOKEN, --token TOKEN
                        your github token. to create new token, go to
                        https://github.com/settings/tokens
  --output-type {csv,json}
                        output type as either csv or json
  -o OUT_FILE, --out-file OUT_FILE
                        name of the output file (default: stargazers)
```
