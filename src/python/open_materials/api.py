#encoding: utf-8
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

import requests
import json

token = "..."

header = {"Authorization": "Bearer" + token, "Accept": "application/vnd.github+json"}
repo = "data"
user = "opensource-construction"
branch = "main"


name_map = {
    "Holz":"Cross_Laminated_Timber_Smartlam", "Beton":"Concrete", 
    "Unterlagsboden":"Concrete", "Schichtex Holzwolle":"Concrete", 
    "Verputz":"Concrete", "Massivbau Beton":"Concrete",
    "Holzfassade 600":"Cross_Laminated_Timber_Stora_Enso", "Holzfassade 600":"Schilliger_cross_laminated_timber",
    "Dämmung":"Wood", "Glas":"Glass", "Metall":"Steel"}
index = {}

def make_index():
    url = f"https://api.github.com/repos/{user}/{repo}/git/trees/{branch}?recursive=1"

    res = requests.get(url, headers=header)
    rjson = res.json()

    for r in rjson["tree"]:
        bn = os.path.basename(r["path"]).split('.')[0]
        index[bn] = r["path"]

    #print("INDEX:")
    #print(index)

def get_material_data(name):
    base_url = f"https://{user}.github.io/{repo}/"

    print(f"Looking for '{name}'")
    if name in name_map.keys():
        name = name_map[name]

    if name not in index.keys():
        name = "Concrete"

    print(f"    found {index[name]}")
    res = requests.get(base_url + index[name])
    return res.json()


def main():
# The API endpoint
    url = "https://opensource-construction.github.io/KBOB/data/Abfalltrennsystem.json"
    url = "https://api.github.com/repos/opensource-construction/KBOB/commits"

    #res = requests.get("https://api.github.com/repos/opensource-construction/KBOB/commits")
    #url = "https://api.github.com/repos/opensource-construction/KBOB/git/tree/data"
    url = f"https://api.github.com/repos/{user}/{repo}/git/trees/{branch}?recursive=1"
   
    base_url = f"https://{user}.github.io/{repo}/"

    # A GET request to the API
    res = requests.get(url, headers=header)
    #print(dir(res))
    #print(res.text.encode('utf-8'))
    #return

    # Print the response
    rjson = res.json()

    for r in rjson["tree"][:6]:
        #print(r)
        bn = os.path.basename(r["path"]).split('.')[0]
        print(bn)
        path = r["path"]
        if path.endswith(".json"):
            path = base_url + r["path"]
            print(f"Path is: {path}")
            #continue
            res = requests.get(base_url + r["path"])
            print(res.json())
            #break

if __name__=="__main__":
    main()