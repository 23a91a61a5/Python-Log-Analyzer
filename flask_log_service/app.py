from flask import Flask, request, jsonify         # Import Flask and helpers for HTTP and JSON
from analyzer import parse_logs, generate_report  # Import your log parsing and reporting functions
from mongodb import reports                       # Import MongoDB collection to store reports

# Create the Flask application
app = Flask(__name__)


# Simple health-check endpoint to see if the service is running
@app.route("/health")
def health():
    # Returns a small JSON saying the service is OK
    return {"status": "ok"}


# Main endpoint to analyze an uploaded log file
@app.route("/analyze", methods=["POST"])
def analyze():

    # 1) Validate: check if a file was sent in the request
    if "file" not in request.files:
        # If not, return an error JSON with HTTP status 400 (Bad Request)
        return jsonify({"error": "No file uploaded"}), 400

    # 2) Get the uploaded file object from the request
    file = request.files["file"]

    # 3) Read the file content as text (UTF-8 decoding)
    content = file.read().decode("utf-8")

    # 4) Use your analyzer function to convert raw text into structured logs
    logs = parse_logs(content)

    # 5) Generate a summary report (counts of INFO, WARNING, ERROR, etc.)
    report = generate_report(logs)

    # 6) Add the original file name to the report
    report["file_name"] = file.filename

    # 7) Save the report to MongoDB collection "reports"
    inserted = reports.insert_one(report)

    # 8) Store the inserted MongoDB ID (converted to string) in the report
    report["report_id"] = str(inserted.inserted_id)

    # 9) Return the report as JSON back to the frontend
    return jsonify(report)


# Endpoint to fetch all stored reports from MongoDB
@app.route("/reports")
def get_reports():

    data = []

    # 1) Loop through all documents in the "reports" collection
    for report in reports.find():

        # Convert the MongoDB ObjectId to string so it is JSON serializable
        report["_id"] = str(report["_id"])

        # Add each report to a list
        data.append(report)

    # 2) Return the list of all reports as JSON
    return jsonify(data)


# This block runs only when we execute "py app.py" directly
if __name__ == "__main__":
    # Start the Flask development server on port 5000 with debug mode enabled
    app.run(port=5000, debug=True)
