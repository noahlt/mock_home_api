from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory state
state = {
    "frontdoor": "locked",
    "blinds": 0.0,
}


@app.route("/frontdoor", methods=["GET"])
def get_frontdoor():
    return jsonify({"status": state["frontdoor"]})


@app.route("/frontdoor/lock", methods=["POST"])
def lock_frontdoor():
    state["frontdoor"] = "locked"
    return jsonify({"status": "locked"})


@app.route("/frontdoor/unlock", methods=["POST"])
def unlock_frontdoor():
    state["frontdoor"] = "unlocked"
    return jsonify({"status": "unlocked"})


@app.route("/blinds", methods=["GET"])
def get_blinds():
    return jsonify({"open": state["blinds"]})


@app.route("/blinds", methods=["POST"])
def set_blinds():
    data = request.get_json()
    if data is None or "open" not in data:
        return jsonify({"error": "Missing 'open' field"}), 400

    value = data["open"]
    if not isinstance(value, (int, float)) or value < 0.0 or value > 1.0:
        return jsonify({"error": "'open' must be a number between 0.0 and 1.0"}), 400

    state["blinds"] = float(value)
    return jsonify({"open": state["blinds"]})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
