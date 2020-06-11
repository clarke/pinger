"""Setup script for pinger"""

import os.path
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as f:
    README = f.read()

setup(
    name                          = 'pinger',
    version                       = '1.0.0',
    description                   = "Check to see if a website is reachable.",
    long_description              = README,
    long_description_content_type = 'text/markdown',
    url                           = 'https://github.com/clarke/pinger',
    author = 'Clarke Retzer',
    author_email = 'clarke@carfoo.com',
    license = 'MIT',
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python 3",
    ],
    packages = ["pinger"],
    include_package_data = True,
    install_request = [
        'requests',
        'pyyaml',
    ],
    entry_points = {
        "console_scripts": ['pinger=pinger_runner.__main__:main']
    },
)
