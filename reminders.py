"""Reminder / follow-up notifications.

TODO: not implemented yet. Intended design (from pitch deck):
  - A daily cron job checks tasks with status != 'Done' and due_date <= today+1
  - Sends a Teams/Outlook message to the owner via Microsoft Graph
  - Escalates to the meeting organizer if overdue by more than 2 days

None of this is wired up yet — ran out of time during the hackathon.
"""


def send_reminders():
    raise NotImplementedError("Reminder logic not implemented yet - see TODO in this file.")
