#!/usr/bin/env python2
import yum
from flask import Flask, abort, jsonify

app = Flask(__name__)


NAME = 'foreman-{repo}-{version}-{dist}-{arch}'
BASEURL = 'https://yum.theforeman.org/{repo}/{version}/{dist}/{arch}/'


@app.route('/<repo>/<version>')
@app.route('/<repo>/<version>/<dist>')
@app.route('/<repo>/<version>/<dist>/<arch>')
def packages(repo, version, dist='el7', arch='x86_64'):
    if repo not in ('plugins', 'releases'):
        abort(400)

    name = NAME.format(repo=repo, arch=arch, dist=dist, version=version)
    baseurl = BASEURL.format(repo=repo, arch=arch, dist=dist, version=version)

    yb = yum.YumBase()
    yb.setCacheDir()

    for repo in yb.repos.listEnabled():
        repo.disable()

    yb.add_enable_repo(name, [baseurl])

    return jsonify({pkg.name: {'version': pkg.version} for pkg in yb.pkgSack.returnNewestByName()})


if __name__ == '__main__':
    app.run(host='::')
