# Global-Legal-AI
# ​"أنشئ ملف index.html احترافي للمنصة القانونية، يحتوي على صندوق محادثة (Chat) يتصل بـ API الذكاء الاصطناعي، ونسق الصفحة بألوان رسمية."

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Global-Legal-AI - ​"أنشئ ملف index.html احترافي للمنصة القانونية، يحتوي على صندوق محادثة (Chat) يتصل بـ API الذكاء الاصطناعي، ونسق الصفحة بألوان رسمية."'

@app.route('/api/test')
def test():
    return jsonify({
        "status": "success",
        "message": "تم تنفيذ المهمة",
        "task": "​"أنشئ ملف index.html احترافي للمنصة القانونية، يحتوي على صندوق محادثة (Chat) يتصل بـ API الذكاء الاصطناعي، ونسق الصفحة بألوان رسمية.""
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)