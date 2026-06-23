from flask import Flask, request, jsonify
from analyzer import parse_logs, generate_report
from mongodb import reports

app = Flask(__name__)


@app.route("/health")
def health():
    return {"status": "ok"}


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


@app.route("/reports")
def get_reports():

    data = []

    for report in reports.find():

        report["_id"] = str(report["_id"])

        data.append(report)

    return jsonify(data)


if __name__ == "__main__":
    app.run(port=5000, debug=True)