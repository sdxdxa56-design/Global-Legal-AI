# Global-Legal-AI
#  اريد اخراج مجلد index.html من ملف templates 

from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return 'Global-Legal-AI -  اريد اخراج مجلد index.html من ملف templates '

@app.route('/api/test')
def test():
    return jsonify({
        "status": "success",
        "task": " اريد اخراج مجلد index.html من ملف templates "
    })

if __name__ == '__main__':
    app.run(debug=True)
