from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        return jsonify(message='Hello, Python Flask API!')
    elif request.method == 'POST':
        # Handle POST request if needed
        return jsonify(message='POST request received!')
    else:
        return jsonify(message='Invalid request method')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
