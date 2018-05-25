# Foreman Packages

This is a work in progress to get more insight into the Foreman Packages. It's divided into 3 services and one task:

## Git

A set of scripts to extract packages and their versions from [foreman-packaging](https://github.com/theforeman/foreman-packaging).

Currently limited to the RPM branches.

## Yum

A service that exposes [Foreman Yum Plugins](https://yum.theforeman.org/plugins/) as a REST interface making it easy to consume in various languages. Implemented as a Python 2 Flask service. It directly uses Yum as a library so it's wrapped in a CentOS 7 container.

## Deb

A service that exposes [Foreman Debian Plugin](https://deb.theforeman.org/) as a REST interface making it easy to consume in various languages. Implemented as a Python 3 Flask srevice. It uses command line tools that are packaged on Debian so it's wrapped in a Debian 9 container.

## Web

The frontend of the service. Implemented as a Python 3 Flask service. It uses JSON files and queries backend services. That's combined into REST endpoints. In the frontend it uses [Vue](https://vuejs.org/) and [Bootstrap](https://getbootstrap.com/) to present this in a nice way.

For upstream sources it can query [Rubygems](https://rubygems.org/) and [NPM](https://www.npmjs.com/). Currently it uses the files Git generates and the Yum backend services. Deb is not yet integrated.
