# -*- coding: utf-8 -*-


from setuptools import find_packages
from setuptools import setup

import fastentrypoints

dependencies = ["click"]

config = {
    "version": "0.1",
    "name": "clicktool",
    "url": "https://github.com/jakeogh/clicktool",
    "license": "ISC",
    "author": "Justin Keogh",
    "author_email": "github.com@v6y.net",
    "description": "Common functions for @click",
    "long_description": __doc__,
    "packages": find_packages(exclude=["tests"]),
    "package_data": {"clicktool": ["py.typed"]},
    "include_package_data": True,
    "zip_safe": False,
    "platforms": "any",
    "install_requires": dependencies,
}

setup(**config)
