from flask import Flask,request,jsonify
import os

app = Flask(__name__)

@app.route("/analyze",methods=["POST"])
def analyze():

    sar = request.files["sar"]
    before = request.files["before"]
    after = request.files["after"]

    sar.save("sar.png")
    before.save("before.png")
    after.save("after.png")

    print("Images received")

    return jsonify({
        "total":200,
        "flooded":75,
        "destroyed":22
    })

app.run(port=5000)
