import csv
import json
import os
from collections import defaultdict

import requests
from jsonschema import FormatChecker
from jsonschema.validators import Draft4Validator as validator


def test_registry():
    configuration = {
        # Id must be unique in extensions.csv.
        'extensions.csv': {'Id': None},
        # Version and Base URL must be unique, within the scope of a given Id, in extension_versions.csv.
        'extension_versions.csv': {'Version': 'Id', 'Base URL': 'Id'},
    }

    # Keep track of extension identifiers, to ensure consistency across files.
    identifiers = {}

    for csv_basename, uniqueness in configuration.items():
        schema_basename = '{}-schema.json'.format(os.path.splitext(csv_basename)[0])

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'schema', schema_basename)) as f:
            schema = json.load(f)

        # Count the occurrences of a key-value pair, within a given scope.
        seen = {}
        for key, scope in uniqueness.items():
            if scope:
                seen[scope] = defaultdict(lambda: defaultdict(set))
            else:
                seen[key] = set()

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', csv_basename)) as f:
            reader = csv.DictReader(f)
            for row in reader:
                id = row['Id']

                for key in reader.fieldnames:
                    if not row[key]:
                        del row[key]

                for error in validator(schema, format_checker=FormatChecker()).iter_errors(row):
                    raise Exception('{}: {} ({})\n'.format(id, error.message, '/'.join(error.absolute_schema_path)))

                # Validate that URLs resolve.
                if row.get('Base URL'):
                    response = requests.get(row['Base URL'] + 'extension.json')
                    response.raise_for_status()
                if row.get('Download URL'):
                    response = requests.get(row['Download URL'])
                    response.raise_for_status()

                # Validate the uniqueness of a key-value pair, within a given scope.
                for key, scope in uniqueness.items():
                    value = row[key]
                    if scope:
                        if value in seen[scope][row[scope]][key]:
                            raise Exception('{}: Duplicate {} "{}" in scope of {} "{}" on line {}'.format(
                                csv_basename, key, value, scope, row[scope], reader.line_num))
                        seen[scope][row[scope]][key].add(value)
                    else:
                        if value in seen[key]:
                            raise Exception('{}: Duplicate {} "{}" on line {}'.format(
                                csv_basename, key, value, reader.line_num))
                        seen[key].add(value)

                if csv_basename == 'extensions.csv':
                    identifiers[id] = 0
                else:
                    # Ensure every version belongs to a known extension.
                    if id in identifiers:
                        identifiers[id] += 1
                    else:
                        raise Exception('extension_versions.csv: Id "{}" not in extensions.csv'.format(id))

    # Ensure every extension has at least one version.
    for id, count in identifiers.items():
        if not count:
            raise Exception('extensions.csv: Id "{}" not in extension_versions.csv'.format(id))
