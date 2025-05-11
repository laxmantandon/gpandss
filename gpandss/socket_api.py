import frappe
import redis

redis_conn = redis.StrictRedis.from_url(frappe.conf.redis_socketio)

@frappe.whitelist()
def on_connect():
    user = frappe.session.user
    redis_conn.set(f"user:{user}:online", "1")

@frappe.whitelist()
def on_disconnect():
    user = frappe.session.user
    redis_conn.set(f"user:{user}:online", "0")

@frappe.whitelist()
def is_user_online():
    user = frappe.session.user
    online_status = redis_conn.get(f"user:{user}:online")
    return online_status