#Authors: Troy House, Joshua Leensvaart
import sys
import argparse
import requests


#WIKI API variable
WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"

def main(argv):
    #An argument parser to the argument for the script that will be the wiki page title
    parser = argparse.ArgumentParser(prog="wiki_recent")
    parser.add_argument("title", help="Wikipedia article title")
    args = parser.parse_args(argv)

    #Query parameters for the wiki page
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": args.title,
        "rvprop": "timestamp|user",
        "rvlimit": "30",
        "redirects": "1"
    }

    #http header
    headers = {
        "User-Agent": "WikiRecentEditsBot/1.0 (troy.house@bsu.edu)"
    }

    #making a request to the page
    try:
        response = requests.get(WIKIPEDIA_API, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        # Print raw JSON
        print(response.text)

    #catches errors
    except requests.RequestException as e:
        print(f"Network error: {e}", file=sys.stderr)
        sys.exit(1)

main(sys.argv[1:])

