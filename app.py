from flask import Flask, jsonify
from flask_cors import CORS

from dashboard.glucose_service import (
    CGM_DIR,
    load_participant_data,
    predict_latest,
)

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Happiest Health Digital Twin API",
        "status": "running",
        "prediction_endpoint": "/api/predict/<participant_id>",
        "participants_endpoint": "/api/participants",
        "history_endpoint": "/api/cgm/<participant_id>",
    })


@app.route("/api/participants", methods=["GET"])
def get_participants():
    try:
        if not CGM_DIR.exists():
            return jsonify({
                "error": "Participant dataset directory not found."
            }), 404

        participants = sorted(
            file.stem
            for file in CGM_DIR.glob("*.csv")
            if file.stem.isalnum()
        )

        if not participants:
            return jsonify({
                "error": "No participant CSV files were found."
            }), 404

        return jsonify({
            "participants": participants,
            "count": len(participants),
        }), 200

    except Exception:
        app.logger.exception("Failed to load participants")
        return jsonify({
            "error": "Unable to load participant list."
        }), 500


@app.route("/api/cgm/<participant_id>", methods=["GET"])
def get_cgm_history(participant_id):
    try:
        data = load_participant_data(participant_id)
        history = data.tail(288)

        readings = [
            {
                "timestamp": row["time"].isoformat(),
                "glucose": float(row["glucose"]),
            }
            for _, row in history.iterrows()
        ]

        return jsonify({
            "participant_id": participant_id,
            "interval_minutes": 5,
            "readings": readings,
        }), 200

    except FileNotFoundError:
        return jsonify({
            "error": "Participant data not found."
        }), 404

    except ValueError as exc:
        return jsonify({
            "error": str(exc)
        }), 400

    except Exception:
        app.logger.exception("Failed to load CGM history")
        return jsonify({
            "error": "Unable to load CGM history."
        }), 500


@app.route("/api/predict/<participant_id>", methods=["GET"])
def predict_glucose(participant_id):
    try:
        result = predict_latest(participant_id)
        return jsonify(result), 200

    except FileNotFoundError:
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