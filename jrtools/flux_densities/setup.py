"""
setup.py -- setup script for use of packages.
"""

from setuptools import setup

install_requires = []

setup(
    name='flux_densities',
    version='1.0',
    packages=['flux_densities'],
    entry_points={
        'console_scripts': [
            'flux_densities=flux_densities:main',
        ],
    },
    install_requires=install_requires,
    url='https://github.com/jrseti/jrtools',
    license='MIT',
    author='Jon Richards',
    author_email='jrseti@gmail.com',
    description='Various Python tools and applications by Jon Richards, jrseti@gmail.com',
    test_suite='nose.collector',
    tests_require=['nose']
)
