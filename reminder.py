import psycopg2
import firebase_admin
from firebase_admin import messaging, credentials
from datetime import datetime, timedelta, timezone
import uuid

# DB CONNECTION
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password="Shruti@123",
    database="postgres"
)
cursor = conn.cursor()

# FCM INIT
cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)


def get_stale_locks():
    cutoff_ts = int((datetime.now(timezone.utc) - timedelta(days=30)).timestamp())

    cursor.execute("""
        SELECT lock_id FROM locks_table
        WHERE last_battery_check_ts < %s
    """, (cutoff_ts,))

    return [row[0] for row in cursor.fetchall()]


def get_user(lock_id):
    cursor.execute("""
        SELECT user_id, fcm_id
        FROM lock_user_mapping
        WHERE lock_id = %s
    """, (lock_id,))
    return cursor.fetchone()


def send_notification(fcm_token, lock_id):
    notification_id = str(uuid.uuid4())

    message = messaging.Message(
        token=fcm_token,
        notification=messaging.Notification(
            title="Battery Check Reminder",
            body=f"Please check your lock ({lock_id}) battery level."
        ),
        data={
            "notification_id": notification_id,
            "lock_id": lock_id,
            "click_action": "https://your-server.com/notification-click"
        }
    )

    messaging.send(message)
    return notification_id


def log_notification(user_id, lock_id, notification_id):
    cursor.execute("""
        INSERT INTO notifications_log (notification_id, user_id, lock_id)
        VALUES (%s, %s, %s)
    """, (notification_id, user_id, lock_id))
    conn.commit()


def main():
    stale_locks = get_stale_locks()

    if not stale_locks:
        print("No stale locks to notify.")
        return

    for lock_id in stale_locks:
        user = get_user(lock_id)
        if not user:
            print(f"No user for lock {lock_id}")
            continue

        user_id, fcm_id = user
        notif_id = send_notification(fcm_id, lock_id)
        log_notification(user_id, lock_id, notif_id)
        print(f"Sent → user {user_id}, lock {lock_id}")

    print("Weekly notifications completed.")


if __name__ == "__main__":
    main()
