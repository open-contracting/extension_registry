from setuptools import setup

setup(
    name='ocdsextensionregistry',
    version='0.0.0',
    packages=['ocdsextensionregistry'],
    install_requires=[
        'jsonschema',
        'requests',
        'rfc3987',
        'strict-rfc3339',
    ],
    extras_require={
        'test': [
            'pytest',
        ]
    },
)
