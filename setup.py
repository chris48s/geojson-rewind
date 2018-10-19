import os
from setuptools import setup

def _get_description():
    try:
        path = os.path.join(os.path.dirname(__file__), 'README.md')
        with open(path, encoding='utf-8') as f:
            return f.read()
    except IOError:
        return ''

setup(
    name='geojson-rewind',
    version='0.1.0',
    author="chris48s",
    license="MIT",
    description='A Python library for enforcing polygon ring winding order in GeoJSON',
    long_description=_get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/chris48s/geojson-rewind",
    packages=['geojson_rewind'],
    extras_require={
        'testing': [
            'python-coveralls',
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
