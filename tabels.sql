CREATE TABLE IF NOT EXISTS locks_table (
    lock_id TEXT PRIMARY KEY,
    last_battery_check_ts BIGINT    -- Unix timestamp (UTC)
);

CREATE TABLE IF NOT EXISTS lock_user_mapping (
    lock_id TEXT,
    user_id TEXT,
    fcm_id TEXT,
    PRIMARY KEY (lock_id)
);

CREATE TABLE IF NOT EXISTS notifications_log (
    notification_id TEXT PRIMARY KEY,
    user_id TEXT,
    lock_id TEXT,
    sent_at TIMESTAMP DEFAULT NOW(),
    clicked BOOLEAN DEFAULT FALSE
);
UPDATE locks_table
SET last_battery_check_ts = EXTRACT(EPOCH FROM NOW()) - 3000000
WHERE lock_id = '<one_existing_lock_id>';
