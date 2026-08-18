import argparse
import os

from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

import db
from transcript_parser import parse_transcript
from summarizer import summarize
from extractor import extract_action_items
from integrator import create_planner_task

load_dotenv()

app = Flask(__name__)


def run_pipeline(transcript_path: str, verbose: bool = True):
    """Runs transcript -> summary -> action items -> (mocked) task creation -> db."""
    turns = parse_transcript(transcript_path)
    if verbose:
        print(f"Parsed {len(turns)} turns from {transcript_path}\n")

    summary = summarize(turns)
    if verbose:
        print("=== SUMMARY ===")
        print(summary, "\n")

    action_items, weak_signals = extract_action_items(turns)

    if verbose:
        print(f"=== ACTION ITEMS ({len(action_items)}) ===")
        for item in action_items:
            print(f"- [{item['owner']}] {item['description']}  (due: {item['due_date']}, "
                  f"due_confidence={item['due_date_confidence']})")

        if weak_signals:
            print(f"\n=== FLAGGED (implicit, no clear owner - {len(weak_signals)}) ===")
            for w in weak_signals:
                print(f"- ({w['speaker']}): {w['text']}")

    db.init_db()
    created = []
    for item in action_items:
        result = create_planner_task(item)
        db.insert_task(item["description"], item["owner"], item["due_date"], result["task_id"])
        created.append(result)

    if verbose:
        print(f"\n=== TASK CREATION (mocked, see integrator.py) ===")
        for c in created:
            print(f"- {c['task_id']} -> status: {c['status']}")

    return {"summary": summary, "action_items": action_items, "weak_signals": weak_signals}


@app.route("/")
def dashboard():
    tasks = db.get_all_tasks()
    return render_template("dashboard.html", tasks=tasks)


@app.route("/tasks/<int:task_id>/status", methods=["POST"])
def update_status(task_id):
    new_status = request.form.get("status", "Open")
    db.update_task_status(task_id, new_status)
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--process", help="Path to a transcript file to run the pipeline on once, via CLI.")
    args = parser.parse_args()

    db.init_db()

    if args.process:
        run_pipeline(args.process)
    else:
        app.run(debug=True, port=5000)
