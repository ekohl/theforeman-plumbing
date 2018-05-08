#!/usr/bin/env python2
from flask import Flask, jsonify
import yum


app = Flask(__name__)


NAME = 'foreman-plugins-{version}-{dist}-{arch}'
BASEURL = 'https://yum.theforeman.org/plugins/{version}/{dist}/{arch}/'


@app.route('/<version>', defaults={'dist': 'el7', 'arch': 'x86_64'})
@app.route('/<version>/<dist>', defaults={'arch': 'x86_64'})
@app.route('/<version>/<dist>/<arch>')
def packages(version, dist, arch):
    name = NAME.format(arch=arch, dist=dist, version=version)
    baseurl = BASEURL.format(arch=arch, dist=dist, version=version)

    yb = yum.YumBase()
    yb.setCacheDir(suffix='/' + name)

    for repo in yb.repos.listEnabled():
        repo.disable()

    repo = yum.yumRepo.YumRepository(name)
    repo.baseurl = baseurl
    repo.enable()

    yb.repos.add(repo)

    return jsonify({pkg.name: {'version': pkg.version} for pkg in yb.pkgSack.returnNewestByName()})


if __name__ == '__main__':
    app.run(host='::')
