import os,json,csv

label_dir="xbd/tier1/labels"
out="data/xbd/labels.csv"

mapping={
    "no-damage":0,
    "minor-damage":1,
    "major-damage":2,
    "destroyed":3
}

rows=[["image","damage"]]

for f in os.listdir(label_dir):

    # ONLY post disaster
    if "post" not in f.lower():
        continue

    with open(os.path.join(label_dir,f)) as file:
        data=json.load(file)

    buildings=data["features"]["lng_lat"]

    # skip empty
    if len(buildings)==0:
        continue

    props=buildings[0]["properties"]

    damage=props.get("subtype") or props.get("damage") or props.get("damage_type")

    if damage not in mapping:
        continue

    img=f.replace(".json",".png")

    rows.append([img,mapping[damage]])

with open(out,"w",newline="") as csvfile:
    csv.writer(csvfile).writerows(rows)

print("labels.csv created:",len(rows)-1,"samples")
