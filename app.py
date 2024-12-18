from flask import Flask, send_from_directory
from api import api_bp 

app = Flask(__name__)

# Frontend
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Assets
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
