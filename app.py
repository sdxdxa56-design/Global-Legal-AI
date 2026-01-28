from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "مرحباً بالمنصة القانونية"
if __name__ == '__main__':
    app.run(port=5000)