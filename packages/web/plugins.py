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


def get_yum_release(release, dist):
    url = 'http://localhost:5001/plugins/{}/{}'.format(release, dist)
    filename = 'git-rpm-{}-{}.json'.format(release, dist)
    return get_release(url, filename)


def get_deb_release(release):
    url = 'http://localhost:5002/plugins/{}'.format(release)
    return get_release(url)


def get_release(url, filename=None):
    response = requests.get(url)
    response.raise_for_status()

    if filename:
        with open(os.path.join(app.static_folder, filename)) as fp:
            git = json.load(fp)
    else:
        git = {}

    return {pkg: {'repo': data['version'], 'git': git.get(pkg)}
            for pkg, data in response.json().items() if not pkg.endswith('-doc')}


@app.route('/')
def index():
    return app.send_static_file('plugins.html')


@app.route('/plugins')
def plugins():
    return app.send_static_file('plugins.json')


@app.route('/releases/<rel>')
def release(rel):
    result = {
        'el7': get_yum_release(rel, 'el7'),
        'deb': get_deb_release(rel),
    }

    return jsonify(result)


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
