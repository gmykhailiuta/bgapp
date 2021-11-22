"""Flask app
"""
import os
import socket
from flask_api import FlaskAPI
from flask import render_template

def create_app():
    app = FlaskAPI(__name__)
    app.config.from_mapping(
        VERSION=os.getenv('VERSION'),
        COLOR=os.getenv('COLOR'))
    return app

app = create_app()

@app.route('/', methods=['GET'])
@app.route('/html', methods=['GET'])
def html():
    hostname = socket.gethostname()
    version = app.config['VERSION']
    color = app.config['COLOR']
    return render_template('root.html',
        hostname=hostname,
        version=app.config['VERSION'],
        color=app.config['COLOR'])


@app.route('/api', methods=['GET'])
def api():
    hostname = socket.gethostname()
    version = app.config['VERSION']
    color = app.config['COLOR']
    return {
        "hostname": hostname,
        "version": version,
        "color": color
        }


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return {}


@app.route('/<path:path>')
def catch_all(path):
    return {"message": "Try /"}
