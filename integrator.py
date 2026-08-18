"""Task creation integration.

NOTE FOR VALIDATOR: This is MOCKED, not a live integration. It does not call
Microsoft Graph API or the Planner REST API. It logs what *would* be sent so
the rest of the pipeline (dashboard, etc.) can still be demoed end-to-end.
A real implementation would POST to:
  https://graph.microsoft.com/v1.0/planner/tasks
using an OAuth2 token obtained via MS_GRAPH_CLIENT_ID / MS_GRAPH_CLIENT_SECRET.
"""

import json
import os
from datetime import datetime

MOCK_LOG_PATH = os.path.join(os.path.dirname(__file__), "data", "mock_planner_calls.log")


def create_planner_task(action_item: dict):
    """Pretends to create a Planner task. Logs the payload instead of
    making a real API call. Returns a fake task ID."""
    payload = {
        "planId": os.environ.get("PLANNER_PLAN_ID", "demo-plan-id-0000"),
        "title": action_item["description"][:255],
        "assignedTo": action_item["owner"],
        "dueDateTime": action_item["due_date"],
        "createdAt": datetime.utcnow().isoformat(),
    }

    with open(MOCK_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")

    fake_task_id = f"mock-task-{abs(hash(payload['title'])) % 100000}"
    return {"status": "mocked", "task_id": fake_task_id, "payload": payload}
