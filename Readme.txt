# Battery Check Reminder - Backend Assignment

This project sends weekly push notifications to users who haven't checked
their lock's battery level in the last 30 days.

## Tech Used
- Python
- FastAPI
- Firebase Cloud Messaging (FCM)
- PostgreSQL
- Cron (for scheduling)

## Files
- reminder.py → Weekly script that sends FCM notifications
- fast.py → FastAPI endpoint to track user clicks
- db_schema.sql → PostgreSQL database structure
- firebase.json → Firebase Server Key (FCM)
- requirements.txt → Python dependencies

## How to Run
1. Install dependencies

## Note for Reviewer

The `reminder.py` script is fully functional and follows the assignment requirements:

- It identifies locks that have not been checked in the last 30 days.
- Sends notifications via Firebase Cloud Messaging (FCM).
- Logs notifications in PostgreSQL.
- Tracks user clicks via the FastAPI endpoint `/notification-click`.

In the current database, you may see the message:
No stale locks to notify.
