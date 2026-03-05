# app.py
from flask import Flask, request, jsonify, render_template, send_from_directory
from pathlib import Path
import pandas as pd
from datetime import datetime
from engine.core import SurveyEngine
import time

app = Flask(__name__, template_folder="templates")

BASE_DIR = Path(__file__).parent
SURVEYS_DIR = BASE_DIR / "surveys"


@app.route("/submit/<survey_id>", methods=["POST"])
def submit_response(survey_id):
    data = request.json

    t1 = time.time()
    engine = SurveyEngine(survey_id)
    result = engine.process_response(data)
    t2 = time.time()

    result['time'] = t2-t1

    return jsonify(result)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route('/assets/<FILE>')
def assets (FILE):
    return send_from_directory('assets',FILE)

@app.route("/api/suspicious")
def get_suspicious():
    all_rows = []

    for survey in SURVEYS_DIR.iterdir():
        file = survey / "suspicious.csv"
        data = survey / "data.csv"
        if file.exists():
            try:
                df_data_columns = pd.read_csv(data, nrows=0).columns.tolist()
                df_data_columns.append('score')
                df = pd.read_csv(file, header=None)
                df.columns = df_data_columns
            except:
                continue
            df["survey_id"] = survey.name
            all_rows.append(df)

    if all_rows:
        return jsonify(pd.concat(all_rows).to_dict(orient="records"))

    return jsonify([])



if __name__ == "__main__":
    app.run(debug=True)