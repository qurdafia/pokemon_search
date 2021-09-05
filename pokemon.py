import json
import requests
import os
import re
import datetime

st = os.stat('data.json')
mtime = st.st_mtime
date_created = datetime.datetime.fromtimestamp(mtime)
date_now = datetime.date.today()

d_file = date_created.day
d_now = date_now.day
delta = d_now - d_file

# if file age is greater than 7 days, get an update from the API server

if delta > 7:
    url_api = 'https://pokeapi.co/api/v2/pokemon?limit=1200&offset=0'

    req = requests.get(url_api)
    pokemon_data = req.json()
    pokemon_data_str = json.dumps(pokemon_data, indent=2)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(pokemon_data, f, ensure_ascii=False, indent=4)


# Loads the json file
with open('data.json', 'r') as read_file:
    data = json.load(read_file)
    pokemon_all = data["results"]

    def search_template(pokemon_data_single):
        for attr, value in pokemon_data_single.items():
            if attr == "id":
                print("Pokemon ID: "+str(value))
            elif attr == "name":
                print("Pokemon Name: "+value.capitalize())
            elif attr == "types":
                types = []
                types.append(value[0]["type"]["name"].capitalize())
                print("Type(s): ")
                for type in types:
                    print(type)
            elif attr == "stats":
                stats = []
                for stat in value:
                    stats.append(stat["base_stat"])
                print("HP: "+str(stats[0]))
                print("Attack: "+str(stats[1]))
                print("Defense: "+str(stats[2]))
                print("Special Attack: "+str(stats[3]))
                print("Special Deffense: "+str(stats[4]))
                print("Speed: "+str(stats[5]))
            elif attr == "location_area_encounters":
                url_api_encounters = value
                req = requests.get(url_api_encounters)
                encounters = req.json()
                enc_list = []
                method_list = []
                for encounter in encounters:
                    # print(encounter["location_area"]["name"])
                    full_str = encounter["location_area"]["name"]
                    sub_str = "kanto"
                    if sub_str in full_str:
                        enc_list.append(encounter["location_area"]["name"])
                        method_list.append(encounter["location_area"]["url"])
                
                print("Encounter(s): ")
                if enc_list:
                    for enc in enc_list:
                        print(enc)
                else:
                    print("-")

                print("Method(s): ")
                if method_list:
                    for method in method_list:
                        url_api_method = method
                        req = requests.get(url_api_method)
                        methods = req.json()
                        print(methods["encounter_method_rates"][0]["encounter_method"]["name"])
                else:
                    print("-")

    # Search Pokemon by name
    def search_pokemon():
        poke = input("Enter name: ")
        search = []
        for pokemon in pokemon_all:
            if pokemon["name"] == poke.lower():
                search.append(pokemon["url"])

        if search:
            print("We found "+poke.capitalize()+"!")
            url_api_single = search[0]
            req = requests.get(url_api_single)
            pokemon_data_single = req.json()
            search_template(pokemon_data_single)
                                
        else:
            print("No luck.")

    # Search Pokemon by ID
    def search_pokemon_id():
        poke = input("Enter id: ")
        search = []
        for pokemon in pokemon_all:
            url = pokemon["url"]
            id_obj = re.search(poke, url)
            if id_obj:
                search.append(url)

        if search:
            print("We found "+poke+"!")
            url_api_single = search[0]
            req = requests.get(url_api_single)
            pokemon_data_single = req.json()
            search_template(pokemon_data_single)
        else:
            print("No luck.")

    def search():
        ui_one = input("Press 1 if search by name, 2 if by ID: ")
        if ui_one == "1":
            search_pokemon()
        elif ui_one == "2":
            search_pokemon_id()
        else:
            print("I can't recognize your input.")

    search()