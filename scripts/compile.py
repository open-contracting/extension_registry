import csv
import json
import os
from collections import defaultdict
from datetime import timedelta
from io import StringIO

import requests
import requests_cache

directory = os.path.dirname(os.path.realpath(__file__))

# Cache requests for extensions data for an hour, for faster development.
requests_cache.install_cache(expire_after=timedelta(hours=1))


def compile_extensions_js():
    """
    Compiles build/extensions.js, which includes the most recent versions of extensions, and which the standard
    documentation reads in order to render lists of community extensions.
    """

    # Collect the possible extension versions to compile.
    extension_versions = defaultdict(list)
    with open(os.path.join(directory, '..', 'extension_versions.csv')) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Ignore v1.1 and v1.1.1 versions, as these are superseded by versions using the new extension.json format.
            if row['Version'] not in ('v1.1', 'v1.1.1'):
                extension_versions[row['Id']].append(row)

    # Collect the extension versions to compile.
    extensions = []
    with open(os.path.join(directory, '..', 'extensions.csv')) as f:
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


def compile_extension_versions_wide_csv():
    """
    Compiles build/extension_versions_wide.csv, which merges extensions.csv and extension_versions.csv, for use cases
    in which data from both is required (e.g. finding all core extensions for a specific version of the standard.)
    """

    extensions = {}
    with open(os.path.join(directory, '..', 'extensions.csv')) as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            extensions[row['Id']] = row

    rows = []
    with open(os.path.join(directory, '..', 'extension_versions.csv')) as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames + [fieldname for fieldname in fieldnames if fieldname not in reader.fieldnames]
        for row in reader:
            # OrderedDict will preserve consistent order.
            row.update(extensions[row['Id']])
            rows.append(row)

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)

    return output.getvalue()


if __name__ == '__main__':
    with open(os.path.join(directory, '..', 'build', 'extensions.js'), 'w') as f:
        f.write(compile_extensions_js())

    with open(os.path.join(directory, '..', 'build', 'extension_versions_wide.csv'), 'w') as f:
        f.write(compile_extension_versions_wide_csv())
