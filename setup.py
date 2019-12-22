"""
setup.py -- setup script for use of packages.
"""
from setuptools import setup, find_namespace_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='jrtools',
    packages=find_namespace_packages(include=['jrtools.*']),
    version='1.0',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'flux_densities=jrtools.flux_densities:main',
        ],
    },
    url='https://github.com/jrseti/jrtools',
    license='MIT',
    author='Jon Richards',
    author_email='jrseti@gmail.com',
    description='Various Python tools and applications by Jon Richards, jrseti@gmail.com',
    test_suite='nose.collector',
    tests_require=['nose']
)
