from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)

TOKEN_RE = re.compile(r"^\d{6,12}:[A-Za-z0-9_-]{20,}$")

def get_client_ip():
    # Render places the public client IP in X-Forwarded-For.
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr or "غير معروف"

def telegram_send(token, chat_id, text):
    if not TOKEN_RE.match(token):
        return False, "صيغة Bot Token غير صحيحة."

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        r = requests.post(
            url,
            data={"chat_id": chat_id, "text": text},
            timeout=15
        )
        data = r.json()
        if r.ok and data.get("ok"):
            return True, "تم إرسال البيانات إلى Telegram."
        return False, data.get("description", "فشل Telegram في إرسال الرسالة.")
    except requests.RequestException:
        return False, "تعذر الاتصال بـ Telegram."

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/send")
def send():
    data = request.get_json(silent=True) or {}

    token = str(data.get("token", "")).strip()
    chat_id = str(data.get("chat_id", "")).strip()
    mode = data.get("mode")

    if not token or not chat_id:
        return jsonify(message="أدخل Bot Token و Chat ID."), 400

    ip = get_client_ip()

    if mode == "exact":
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
            return jsonify(message="لم يتم استلام الموقع الدقيق."), 400

        text = (
            "📍 بيانات أرسلها المستخدم بعد موافقته على مشاركة الموقع الدقيق\n\n"
            f"IP: {ip}\n"
            f"Latitude: {latitude}\n"
            f"Longitude: {longitude}\n"
            f"Google Maps: https://www.google.com/maps?q={latitude},{longitude}"
        )

    elif mode == "approx":
        try:
            geo = requests.get(
                f"https://ipwho.is/{ip}",
                timeout=10
            ).json()
        except requests.RequestException:
            geo = {}

        if geo.get("success") is True:
            text = (
                "🌐 بيانات الموقع التقريبي عبر IP\n\n"
                f"IP: {ip}\n"
                f"الدولة: {geo.get('country', 'غير معروف')}\n"
                f"المنطقة: {geo.get('region', 'غير معروف')}\n"
                f"المدينة: {geo.get('city', 'غير معروف')}\n"
                f"الإحداثيات التقريبية: {geo.get('latitude', '?')}, {geo.get('longitude', '?')}\n"
                f"مزود الإنترنت: {geo.get('connection', {}).get('isp', 'غير معروف')}"
            )
        else:
            text = f"🌐 الموقع التقريبي عبر IP\n\nIP: {ip}\nتعذر تحديد الموقع التقريبي."

    else:
        return jsonify(message="طلب غير صالح."), 400

    ok, message = telegram_send(token, chat_id, text)
    return jsonify(message=message), 200 if ok else 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
