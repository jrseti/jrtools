"""
setup.py -- setup script for use of packages.
"""
from setuptools import setup, find_namespace_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Not using 'packages=find_namespace_packages(include=['jrtools.*'])',
# but instead 'packages=['jrtools.flux_densities', 'jrtools.quick_chart']'.
# The reason is that setuptools.find_namespace_packages is not available
# on some pthon distributions. Listing them all manually is better anyway.
setup(
    name='jrtools',
    packages=['jrtools.flux_densities', 'jrtools.quick_chart'],
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
