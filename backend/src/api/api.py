from flask import Flask, jsonify
from experiment_api import experiment_api
from user_management_api import user_management_api
from odm_api import odm_api

app = Flask(__name__)
app.register_blueprint(experiment_api)
app.register_blueprint(user_management_api)
app.register_blueprint(odm_api)


@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'running'})
