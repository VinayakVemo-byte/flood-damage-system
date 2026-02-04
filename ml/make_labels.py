import os,json,csv

label_dir="xbd/tier1/labels"
before_dir="data/xbd/before"
after_dir="data/xbd/after"
out="data/xbd/labels.csv"

mapping={
    "no-damage":0,
    "minor-damage":1,
    "major-damage":2,
    "destroyed":3
}

rows=[["id","damage"]]
count=0

for f in os.listdir(label_dir):

    if "post" not in f.lower():
        continue

    base=f.replace("_post_disaster.json","")

    before_img=f"{base}_pre_disaster.png"
    after_img=f"{base}_post_disaster.png"

    # CHECK images exist
    if not os.path.exists(os.path.join(before_dir,before_img)):
        continue
    if not os.path.exists(os.path.join(after_dir,after_img)):
        continue

    with open(os.path.join(label_dir,f)) as file:
        data=json.load(file)

    buildings=data["features"]["lng_lat"]
    if len(buildings)==0:
        continue

    props=buildings[0]["properties"]
    damage=props.get("subtype") or props.get("damage") or props.get("damage_type")

    if damage not in mapping:
        continue

    rows.append([base,mapping[damage]])
    count+=1

with open(out,"w",newline="") as csvfile:
    csv.writer(csvfile).writerows(rows)

print("labels.csv created:",count,"samples")
