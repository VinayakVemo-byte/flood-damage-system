from flask import Flask,request,jsonify,send_file
import os,cv2
import numpy as np

from flood_model import predict_flood
from building_stats import analyze_buildings

app = Flask(__name__)

os.makedirs("runtime/inputs",exist_ok=True)
os.makedirs("runtime/outputs",exist_ok=True)

def flood_processing(before,after):

    b=cv2.imread(before)
    a=cv2.imread(after)

    diff=cv2.absdiff(b,a)
    gray=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    _,mask=cv2.threshold(gray,30,255,cv2.THRESH_BINARY)

    flooded=int(np.sum(mask>0))
    total=mask.shape[0]*mask.shape[1]
    flood_percent=round(flooded*100/total,2)

    cv2.imwrite("runtime/outputs/mask.png",mask)

    overlay=a.copy()
    overlay[mask>0]=(0,0,255)

    combined=cv2.addWeighted(overlay,0.4,a,0.6,0)
    cv2.imwrite("runtime/outputs/overlay.png",combined)

    return flood_percent,flooded

@app.route("/analyze",methods=["POST"])
def analyze():

    before=request.files["before"]
    after=request.files["after"]
    after_name=request.form.get("after_name")

    before_path="runtime/inputs/before.png"
    after_path="runtime/inputs/after.png"

    before.save(before_path)
    after.save(after_path)

    actual_flood,flood_pixels=flood_processing(before_path,after_path)

    predicted_flood=predict_flood(before_path,after_path)

    building_counts={"no-damage":0,"minor-damage":0,"major-damage":0,"destroyed":0}

    if after_name:
        json_name=after_name.replace(".png",".json")
        json_path=os.path.join("xbd/tier3/labels",json_name)
        if os.path.exists(json_path):
            building_counts=analyze_buildings(json_path)

    return jsonify({
        "actual_flood":actual_flood,
        "predicted_flood":predicted_flood,
        "flood_pixels":flood_pixels,
        "building_counts":building_counts,
        "mask_url":"http://localhost:5000/mask",
        "overlay_url":"http://localhost:5000/overlay"
    })

@app.route("/mask")
def mask():
    return send_file("runtime/outputs/mask.png",mimetype="image/png")

@app.route("/overlay")
def overlay():
    return send_file("runtime/outputs/overlay.png",mimetype="image/png")

if __name__=="__main__":
    app.run(port=5000,debug=True)
