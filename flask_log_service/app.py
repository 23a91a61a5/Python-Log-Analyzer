from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import parse_logs, generate_report
from mongodb import reports

# Create the Flask application
app = Flask(__name__)
CORS(app)  # Allow requests from your frontend


# Simple health-check endpoint to see if the service is running
@app.route("/health")
def health():
    return {"status": "ok"}


# Main endpoint to analyze an uploaded log file
@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    content = file.read().decode("utf-8")

    logs = parse_logs(content)
    report = generate_report(logs)

    report["file_name"] = file.filename

    inserted = reports.insert_one(report)
    report["report_id"] = str(inserted.inserted_id)

    return jsonify(report)


# Endpoint to fetch all stored reports from MongoDB
@app.route("/reports")
def get_reports():
    data = []

    for report in reports.find():
        report["_id"] = str(report["_id"])
        data.append(report)

    return jsonify(data)


if __name__ == "__main__":
    app.run(port=5000, debug=True)