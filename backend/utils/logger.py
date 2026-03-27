from models.activity_log import ActivityLog

def log_activity(db, user_id, action):
    print("🔥 LOGGING:", user_id, action)   # 👈 ADD THIS LINE

    log = ActivityLog(user_id=user_id, action=action)
    db.add(log)
    db.commit()