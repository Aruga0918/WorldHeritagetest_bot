import requests
def get_description(title):
    S = requests.Session()
    URL = "https://ja.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1"
    PARAMS = {
        "titles": title
    }
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    try:
        pageid = list(DATA['query']['pages'].keys())[0]
        return DATA['query']['pages'][str(pageid)]['extract']
    except:
        return "no wiki"
if __name__ == "__main__":
   print(get_description("サグラダファミリア"))