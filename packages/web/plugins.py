import json
import os

import requests

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('plugins.html')


@app.route('/plugins')
def plugins():
    return app.send_static_file('plugins.json')


@app.route('/releases/<rel>/yum/<dist>')
def release(rel, dist):
    response = requests.get('http://localhost:5001/{}/{}'.format(rel, dist))
    response.raise_for_status()

    with open(os.path.join(app.static_folder, 'git-{}-{}.json'.format(rel, dist))) as fp:
        git = json.load(fp)

    results = {pkg: {'repo': data['version'], 'git': git.get(pkg)}
               for pkg, data in response.json().items() if not pkg.endswith('-doc')}
    return jsonify(results)
