import os,cv2,csv
import numpy as np
from tqdm import tqdm

BEFORE="data/xbd/before"
AFTER="data/xbd/after"
OUT="data/xbd/flood_labels.csv"

files = [f for f in os.listdir(AFTER) if f.endswith(".png")]

rows=[["id","flood"]]

print("Total images:",len(files))

for f in tqdm(files):

    base=f.replace("_post_disaster.png","")

    b=f"{BEFORE}/{base}_pre_disaster.png"
    a=f"{AFTER}/{base}_post_disaster.png"

    if not os.path.exists(b):
        continue

    before=cv2.imread(b)
    after=cv2.imread(a)

    diff=cv2.absdiff(before,after)
    gray=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    _,mask=cv2.threshold(gray,30,255,cv2.THRESH_BINARY)

    flooded=np.sum(mask>0)
    total=mask.shape[0]*mask.shape[1]

    flood=round(flooded*100/total,2)

    rows.append([base,flood])

with open(OUT,"w",newline="") as f:
    csv.writer(f).writerows(rows)

print("\nFlood labels created:",len(rows))
print("Saved to:",OUT)
