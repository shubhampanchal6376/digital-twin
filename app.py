from flask import Flask, jsonify, request

from dashboard.glucose_service import predict_latest

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Happiest Health Digital Twin API",
        "status": "running",
        "prediction_endpoint": "/api/predict/<participant_id>",
    })


@app.route("/api/predict/<participant_id>", methods=["GET"])
def predict_glucose(participant_id):
    try:
        result = predict_latest(participant_id)
        return jsonify(result), 200

    except FileNotFoundError as exc:
        app.logger.exception("Required file not found")
        return jsonify({
            "error": "Model or participant data not found."
        }), 404

    except ValueError as exc:
        return jsonify({
            "error": str(exc)
        }), 400
    
    except Exception:
        app.logger.exception("Prediction request failed")
        return jsonify({
            "error": "Prediction failed due to an internal error."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)