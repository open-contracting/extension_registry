#!/usr/bin/env python

from distutils.core import setup

setup(name='ocdsextensionregistry',
      version='0.0',
      description='Process data in OCDS extension repository',
      author='Open Contracting',
      url='',
      packages=['ocdsextensionregistry'],
      package_data={'ocdsextensionregistry': [
              'extension-schema.json'
          ]},
      include_package_data=True,
      )
