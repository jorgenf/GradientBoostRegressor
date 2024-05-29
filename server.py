from flask import Flask, request, jsonify
import xboostregressor as m

app = Flask(__name__)


model = m.Model()

@app.route("/")
def home():
    return "Fish predictor"

@app.route("/get-prediction/<date>")
def prediction(date):
    pred = model.predict(date)
    pred.index = pred.index.strftime("%d-%m-%y")
    print(pred.to_dict())
    return jsonify(pred.to_dict()), 200

def run_server():
    print("running server")
    model.train()
    app.run(debug=True)

