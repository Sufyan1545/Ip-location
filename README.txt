الملفات:
app.py
requirements.txt
render.yaml
templates/index.html

النشر:
1) أنشئ مستودع GitHub جديدًا.
2) ارفع الملفات مع الحفاظ على مجلد templates.
3) في Render اختر New > Web Service.
4) اربط مستودع GitHub.
5) Runtime/Language: Python.
6) Build Command: pip install -r requirements.txt
7) Start Command: gunicorn app:app
8) اختر Free.
9) أنشئ الخدمة وانتظر اكتمال Deploy.
10) افتح رابط onrender.com.

ملاحظات:
- التطبيق لا يحفظ IP أو الموقع أو Bot Token في قاعدة بيانات أو ملف.
- Bot Token يمر عبر الخادم لإرسال الرسالة إلى Telegram، لذلك استخدم الموقع مع مستخدمين موثوقين.
- Render Free قد يوقف الخدمة عند عدم وجود زيارات، وقد يستغرق تشغيلها مجددًا نحو دقيقة.
