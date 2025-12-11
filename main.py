from fastapi import FastAPI, Query
import psycopg2

app = FastAPI()


conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password="Shruti@123",
    database="postgres"
)
cursor = conn.cursor()


@app.get("/notification-click")
def clicked(notification_id: str = Query(...)):
    """
    Mark a notification as clicked in the database
    """
    cursor.execute("""
        UPDATE notifications_log
        SET clicked = TRUE
        WHERE notification_id = %s
    """, (notification_id,))
    conn.commit()
    return {"status": "OK", "notification_id": notification_id}
