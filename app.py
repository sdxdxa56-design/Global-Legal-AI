# Global-Legal-AI
# ​"استخرج كود الـ HTML من ملف app.py وضعه في ملف منفصل تماماً باسم index.html، ثم ارفعه فوراً للمجلد الرئيسي."

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Global-Legal-AI - ​"استخرج كود الـ HTML من ملف app.py وضعه في ملف منفصل تماماً باسم index.html، ثم ارفعه فوراً للمجلد الرئيسي."'

@app.route('/api/test')
def test():
    return jsonify({
        "status": "success",
        "message": "تم تنفيذ المهمة",
        "task": "​"استخرج كود الـ HTML من ملف app.py وضعه في ملف منفصل تماماً باسم index.html، ثم ارفعه فوراً للمجلد الرئيسي.""
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)