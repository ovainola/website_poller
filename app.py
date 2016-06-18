import logging
import platform
from poller import WebPoller, logger_webpoller_factory
from flask import Flask
app = Flask(__name__)
import numpy as np
from flask import render_template, url_for, send_from_directory, jsonify, abort

current_system = platform.system()
if current_system not in ["Windows", "Linux"]:
    raise SystemError("Sorry, could not recognize your system. Terminating program")

webpoller, logger = logger_webpoller_factory("settings.conf")
webpoller.start()

def change_to_json(poll_values):
    """
    """
    all_vals = []
    for name, site_vals in poll_values.items():
        as_json = {}
        as_json["name"] = name
        as_json["connected"] = site_vals["connected"]
        as_json["response_time"] = np.round(site_vals["response_time"], 3)
        as_json["status_code"] = site_vals["status_code"]
        as_json["rule_output"] = []
        for rule_name, output_ in site_vals["rule_output"].items():
            r_output = {}
            r_output["name"] = rule_name
            r_output["output"] = output_
            as_json["rule_output"].append(r_output)
        all_vals.append(as_json)
    return all_vals


@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template('index.html')

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('./templates/css/', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('./templates/js/', path)

@app.route('/poll_backend', methods=['GET', 'POST'])
def poll_backend():
    logger.info("Frontend requesting data")
    data = webpoller.poll_results()
    json_data = change_to_json(data)
    return jsonify(json_data)

if __name__ == "__main__":
    local_url = '0.0.0.0'
    port = 5000
    print("Starting Flask server: http://{0}:{1}".format(local_url, port))
    app.run()
