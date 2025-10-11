import json
import ssl
import urllib.request
import urllib.error
import argparse

def get_wikipedia_data(title):
    """Fetch raw Wikipedia JSON data for a given article title."""
    context = ssl._create_unverified_context()
    base_url = (
        "https://en.wikipedia.org/w/api.php?"
        "action=query&format=json&prop=revisions"
        f"&titles={title.replace(' ', '_')}"
        "&rvprop=timestamp|user&rvlimit=30&redirects=1"
    )
    headers = {
        "User-Agent": "TroyHouseWikiRecentBot/1.0 (troy.house@bsu.edu)"
    }
    req = urllib.request.Request(base_url, headers=headers)
    with urllib.request.urlopen(req, context=context) as response:
        raw_data = response.read().decode()
        return json.loads(raw_data)

def main():
    parser = argparse.ArgumentParser(prog="wiki_recent")
    parser.add_argument("title", help="Wikipedia article title")
    args = parser.parse_args()

    try:
        parsed = get_wikipedia_data(args.title)
        if "query" in parsed and "redirects" in parsed["query"]:
            redirect_to = parsed["query"]["redirects"][0]["to"]
            print(f"Redirected to {redirect_to}")
        print(json.dumps(parsed, separators=(",", ":")))
    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason}")
       
if __name__ == "__main__":
    main()

