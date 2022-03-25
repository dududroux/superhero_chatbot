from urllib.request import urlopen
import json
import pandas as pd
import numpy as np

url = "https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json"
response = urlopen(url)
Marvel = ['Marvel Comics','Archangel','Tempest', 'Giant-Man', 'Toxin', 'Angel', 'Goliath', 'Meltdown','Gemini V','Binary', 'Evil Deadpool', 'Deadpool','Phoenix', 'Power Woman', 'Iron Lad','Power Man','Boom-Boom', 'She-Thing', 'Jean Grey', 'Spider-Carnage', 'Venom III','Ms Marvel II', 'Angel Salvadore', 'Rune King Thor', 'Anti-Venom', 'Scorpion', 'Vindicator II', 'Anti-Vision', 'Thunderbird II', 'Ant-Man']
DC = ['DC Comics', 'Oracle', 'Spoiler', 'Nightwing', 'Black Racer', 'Speed Demon', 'Impulse', 'Batgirl III', 'Flash IV', 'Batgirl V', 'Batman II', 'Batgirl', 'Robin II', 'Robin III', 'Red Hood', 'Red Robin', 'Aztar', 'Superman Prime One-Million']
data_json = pd.DataFrame(json.loads(response.read()))
data_json["intelligence"] = [a["intelligence"] for a in data_json["powerstats"]]
data_json["strength"] = [a["strength"] for a in data_json["powerstats"]]
data_json["speed"] = [a["speed"] for a in data_json["powerstats"]]
data_json["durability"] = [a["durability"] for a in data_json["powerstats"]]
data_json["power"] = [a["power"] for a in data_json["powerstats"]]
data_json["combat"] = [a["combat"] for a in data_json["powerstats"]]
data_json["gender"] = [a["gender"] for a in data_json["appearance"]]
data_json["race"] = [a["race"] for a in data_json["appearance"]]
data_json["height"] = [a["height"][1] for a in data_json["appearance"]]
data_json["eyeColor"] = [a["eyeColor"] for a in data_json["appearance"]]
data_json["hairColor"] = [a["hairColor"] for a in data_json["appearance"]]
data_json["height"] = [a["height"][1] for a in data_json["appearance"]]
data_json["fullName"] = [a["fullName"] for a in data_json["biography"]]
data_json["alterEgos"] = [a["alterEgos"] for a in data_json["biography"]]
data_json["aliases"] = [a["aliases"] for a in data_json["biography"]]
data_json["placeOfBirth"] = [a["placeOfBirth"] for a in data_json["biography"]]
data_json["firstAppearance"] = [a["firstAppearance"] for a in data_json["biography"]]
data_json["publisher"] = [a["publisher"] for a in data_json["biography"]]
data_json["alignment"] = [a["alignment"] for a in data_json["biography"]]
data_json["occupation"] = [a["occupation"] for a in data_json["work"]]
data_json["base"] = [a["base"] for a in data_json["work"]]
data_json["groupAffiliation"] = [a["groupAffiliation"].replace(";", ',').split(',') for a in data_json["connections"]]
data_json["relatives"] = [a["relatives"].replace(";", ',').split(',') for a in data_json["connections"]]
data_json["images"] = [a["sm"] for a in data_json["images"]]
data_json = data_json.drop(["appearance", "biography", "work", "connections"], axis = 1)
data_json = data_json.replace({None: "-"})
data_json = data_json.replace({"": "-"})
data_json["publisher"] = ["Marvel Comics" if (i in Marvel) else i for i in data_json["publisher"]]
data_json["publisher"] = ["DC Comics" if (i in DC) else i for i in data_json["publisher"]]
#data_json = data_json.drop_duplicates(["name"])
reco = data_json.copy().drop(["powerstats"], axis = 1)


for i in pd.Series.unique(reco["publisher"]):
    reco[i] = [1 if (a == i) else 0 for a in reco["publisher"]]
for i in pd.Series.unique(reco["alignment"]):
        reco[i] = [1 if (a == i) else 0 for a in reco["alignment"]]
for i in pd.Series.unique(data_json["gender"]):
        reco[i] = [1 if (a == i) else 0 for a in reco["gender"]]

df = reco.drop(["name", "slug", "images", "alterEgos", "aliases", "placeOfBirth", "firstAppearance"
                     , "alignment", "publisher", "occupation", "base", "groupAffiliation", "relatives", "race", "gender"
                     ,"height" , "eyeColor", "hairColor", "fullName"], axis = 1)

