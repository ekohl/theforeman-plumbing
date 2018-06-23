#!/usr/bin/env python3
import subprocess
import zlib

import requests

from flask import Flask, jsonify

app = Flask(__name__)


BASEURL = 'https://deb.theforeman.org/dists/{distribution}/{version}/binary-{arch}/Packages.gz'
COMMAND = ['grep-dctrl', '-s', 'Package,Version', '']


def get_packages(lines):
    package = None
    for line in lines.split('\n'):
        if line:
            key, value = line.split(': ', 1)
            if key == 'Package':
                package = value
            elif key == 'Version':
                yield package, value.split('-', 1)[0]
        else:
            package = None


@app.route('/<distribution>/<version>')
@app.route('/<distribution>/<version>/<arch>')
def packages(distribution, version, arch='amd64'):
    response = requests.get(BASEURL.format(distribution=distribution, version=version, arch=arch))
    response.raise_for_status()

    data = zlib.decompress(response.content, zlib.MAX_WBITS | 32)

    process = subprocess.Popen(COMMAND, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output = process.communicate(data)[0].decode('utf-8')

    pkgs = dict(get_packages(output))

    return jsonify({pkg: {'version': version} for pkg, version in pkgs.items()})


if __name__ == '__main__':
    app.run(host='::')
