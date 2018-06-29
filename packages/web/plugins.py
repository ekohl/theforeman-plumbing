import json
import os

import requests

from flask import Flask, abort, jsonify

app = Flask(__name__)


PREFIXES = {
    'tfm-rubygem-': 'rubygem',
    'rubygem-': 'rubygem',
    'nodejs-': 'nodejs',
}


@app.route('/')
def index():
    return app.send_static_file('plugins.html')


@app.route('/plugins')
def plugins():
    return app.send_static_file('plugins.json')


@app.route('/releases/<rel>/yum/<dist>')
def release(rel, dist):
    response = requests.get('http://localhost:5001/plugins/{}/{}'.format(rel, dist))
    response.raise_for_status()

    with open(os.path.join(app.static_folder, 'git-{}-{}.json'.format(rel, dist))) as fp:
        git = json.load(fp)

    results = {pkg: {'repo': data['version'], 'git': git.get(pkg)}
               for pkg, data in response.json().items() if not pkg.endswith('-doc')}
    return jsonify(results)


@app.route('/upstream/<package>')
def upstream(package):
    for prefix, package_type in PREFIXES.items():
        if package.startswith(prefix):
            name = package[len(prefix):]
            break
    else:
        # TODO: integrate release-monitoring.org?
        package_type = None

    if package_type == 'rubygem':
        url = 'https://rubygems.org/api/v1/gems/{}.json'.format(name)

        def get_version(data):
            return data['version']
    elif package_type == 'nodejs':
        url = 'https://api.npms.io/v2/package/{}'.format(name)

        def get_version(data):
            return data['collected']['metadata']['version']
    else:
        abort(400)

    response = requests.get(url)
    if response.status_code == 404:
        abort(404)
    response.raise_for_status()
    version = get_version(response.json())

    response = jsonify(version)
    response.cache_control.max_age = 3600
    response.cache_control.public = True
    return response
