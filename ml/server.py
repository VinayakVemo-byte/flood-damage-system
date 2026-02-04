from flask import Flask,request,jsonify,send_file
from flood_from_xbd import detect_flood
from damage_model import predict_damage
import traceback,os

app = Flask(__name__)

INP = "runtime/inputs"
OUT = "runtime/outputs"

os.makedirs(INP, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

@app.route("/analyze",methods=["POST"])
def analyze():

    try:
        before=request.files["before"]
        after=request.files["after"]

        before_path = os.path.join(INP,"before.png")
        after_path = os.path.join(INP,"after.png")

        before.save(before_path)
        after.save(after_path)

        flood,flood_pixels = detect_flood(before_path,after_path)
        damage = predict_damage(before_path,after_path)

        affected_buildings = int(flood_pixels / 400)  # simple estimate

        return jsonify({
            "flood_percent": flood,
            "flood_pixels": flood_pixels,
            "affected_buildings": affected_buildings,
            "damage": damage,
            "mask_url":"http://localhost:5000/mask",
            "overlay_url":"http://localhost:5000/overlay"
        })


    except:
        print(traceback.format_exc())
        return jsonify({"error":"ML failed"}),500


@app.route("/mask")
def mask():
    return send_file(os.path.join(OUT,"flood_mask.png"), mimetype="image/png")

@app.route("/overlay")
def overlay():
    return send_file(os.path.join(OUT,"overlay.png"), mimetype="image/png")

app.run(port=5000,debug=True)
