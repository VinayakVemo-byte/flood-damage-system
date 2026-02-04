from flask import Flask,request,jsonify

app = Flask(__name__)

@app.route("/analyze",methods=["POST"])
def analyze():
    return jsonify({
        "total":200,
        "flooded":75,
        "destroyed":22
    })

app.run(port=5000)
