import os

from flask import Flask, request, jsonify

from adapter import Adapter

app = Flask(__name__)


@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())


@app.route('/', methods=['POST'])
def call_adapter():
    data = request.get_json()
    if data == '':
        data = {}
    adapter = Adapter(data)
    return jsonify(adapter.result)


if __name__ == '__main__':
    if not os.environ.get('BEARER_TOKEN'):
        print('BEARER_TOKEN not set, quitting')
    else:
        app.run(debug=True, host='0.0.0.0', port='8080', threaded=True)
