import csv
import json
import os
from collections import defaultdict

import requests


def compile_registry():
    # Collect the possible extension versions to compile.
    extension_versions = defaultdict(list)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'extension_versions.csv')) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Ignore v1.1 and v1.1.1 versions, as these are superseded by versions using the new extension.json format.
            if row['Version'] not in ('v1.1', 'v1.1.1'):
                extension_versions[row['Id']].append(row)

    # Collect the extension versions to compile.
    extensions = []
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'extensions.csv')) as f:
        reader = csv.DictReader(f)
        for row in reader:
            versions = extension_versions[row['Id']]

            # Prefer frozen versions to live versions.
            frozen_versions = list(filter(lambda version: version['Date'], versions))
            if frozen_versions:
                versions = frozen_versions

            # Get the most recent frozen version. We presently have no strategy for choosing between live versions.
            version = max(versions, key=lambda version: version['Date'])

            data = requests.get(version['Base URL'] + 'extension.json').json()

            extensions.append({
                'category': row['Category'],
                'core': row['Core'] == 'true',
                'url': version['Base URL'],
                'name': {
                    'en': data['name']['en'],
                },
                'description': {
                    'en': data['description']['en'],
                },
                'documentation_url': data['documentationUrl']['en'],
            })

    return 'extensions_callback({})'.format(json.dumps({'extensions': extensions}, sort_keys=True))


if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'build', 'extensions.js'), 'w') as f:
        f.write(compile_registry())
