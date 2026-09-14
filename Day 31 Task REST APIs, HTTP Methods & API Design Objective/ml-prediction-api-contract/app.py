from flask import Flask, request, jsonify

app = Flask(__name__)

model_loaded = True

@app.route("/health", methods=["GET"])
def health():
    if model_loaded:
        return jsonify({"status": "ok", "model_loaded": True}), 200
    else:
        return jsonify({"status": "error", "message": "Model is not loaded yet"}), 503

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if data is None or "features" not in data or not isinstance(data["features"], list):
        return jsonify({"error": "Bad Request", "message": "features field is required and must be a list of numbers"}), 400

    features = data["features"]

    total = sum(features)
    if total < 10:
        prediction = "setosa"
    elif total < 20:
        prediction = "versicolor"
    else:
        prediction = "virginica"

    confidence = 0.97

    return jsonify({"prediction": prediction, "confidence": confidence}), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found", "message": "The requested endpoint does not exist"}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method Not Allowed", "message": "This endpoint does not support the requested HTTP method"}), 405

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
