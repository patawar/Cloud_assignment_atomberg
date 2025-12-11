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
@app.get("/campaign-stats")
def campaign_stats():
    cursor.execute("""
        SELECT 
            COUNT(*) FILTER (WHERE clicked = TRUE) AS clicks,
            COUNT(*) AS sent,
            CASE WHEN COUNT(*) = 0 THEN 0
                 ELSE ROUND(
                        (COUNT(*) FILTER (WHERE clicked = TRUE)::numeric / 
                         COUNT(*)::numeric) * 100, 2
                     )
            END AS ctr_percentage
        FROM notifications_log
        WHERE sent_at > NOW() - INTERVAL '7 days';
    """)

    clicks, sent, ctr = cursor.fetchone()

    return {
        "notifications_sent": sent,
        "notifications_clicked": clicks,
        "ctr_percentage": f"{ctr}%"
    }
