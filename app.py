import logging
import platform
from poller import WebPoller, logger_webpoller_factory
from flask import Flask
app = Flask(__name__)
from flask import render_template, url_for, send_from_directory, jsonify, abort

current_system = platform.system()
if current_system not in ["Windows", "Linux"]:
    raise SystemError("Sorry, could not recognize your system. Terminating program")

webpoller, logger = logger_webpoller_factory("settings.conf")
#webpoller.start()


@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template('index.html')

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('./templates/css/', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('./templates/js/', path)

@app.route('/test', methods=['GET', 'POST'])
def rest_test():
    return jsonify({"success": 1})


if __name__ == "__main__":
    local_url = '0.0.0.0'
    port = 5000
    print("Starting Flask server: http://{0}:{1}".format(local_url, port))

    app.run()
