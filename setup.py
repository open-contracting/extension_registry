from setuptools import setup, find_packages

setup(
    name='ocdsextensionregistry',
    version='0.0.0',
    packages=find_packages(),
    install_requires=[
        'jsonschema',
        'requests',
        'rfc3987',
        'strict-rfc3339',
    ],
    extras_require={
        'test': [
            'pytest',
        ],
    },
)
