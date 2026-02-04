import os,shutil

src="xbd/tier1/images"
before="data/xbd/before"
after="data/xbd/after"

os.makedirs(before,exist_ok=True)
os.makedirs(after,exist_ok=True)

for f in os.listdir(src):
    n=f.lower()
    if "pre" in n:
        shutil.copy(src+"/"+f,before+"/"+f)
    elif "post" in n:
        shutil.copy(src+"/"+f,after+"/"+f)

print("Split done")
