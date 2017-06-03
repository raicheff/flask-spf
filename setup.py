#
# Flask-SPF
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


from setuptools import find_packages, setup


setup(
    name='Flask-SPF',
    version='0.1.0',
    description='Flask-SPF',
    author='Boris Raicheff',
    author_email='b@raicheff.com',
    url='https://github.com/raicheff/flask-spf',
    install_requires=('flask', 'six', 'beautifulsoup4'),
    packages=find_packages(),
)


# EOF
