import csv
import json
import os
from collections import defaultdict

from jsonschema import FormatChecker
from jsonschema.validators import Draft4Validator as validator


def validate_registry_csv(extensions_path, extension_versions_path):
    configuration = (
        # Id must be unique in extensions file.
        (extensions_path, 'extension-schema.json', {'Id': None}),
        # Version and Base URL must be unique, within the scope of a given Id, in extension versions file.
        (extension_versions_path, 'extension-version-schema.json', {'Version': 'Id', 'Base URL': 'Id'}),
    )

    # Keep track of extension identifiers, to ensure consistency across files.
    identifiers = {}

    for data_file, schema_file, uniqueness in configuration:
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), schema_file)) as f:
            schema = json.load(f)

        # Count the occurrences of a key-value pair, within a given scope.
        seen = {}
        for key, scope in uniqueness.items():
            if scope:
                seen[scope] = defaultdict(lambda: defaultdict(set))
            else:
                seen[key] = set()

        with open(data_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                id = row['Id']

                for key in reader.fieldnames:
                    if not row[key]:
                        del row[key]

                for error in validator(schema, format_checker=FormatChecker()).iter_errors(row):
                    raise Exception('{}: {} ({})\n'.format(id, error.message, '/'.join(error.absolute_schema_path)))

                # Validate the uniqueness of a key-value pair, within a given scope.
                for key, scope in uniqueness.items():
                    value = row[key]
                    if scope:
                        if value in seen[scope][row[scope]][key]:
                            raise Exception('{}: Duplicate {} "{}" in scope of {} "{}" on line {}'.format(
                                data_file, key, value, scope, row[scope], reader.line_num))
                        seen[scope][row[scope]][key].add(value)
                    else:
                        if value in seen[key]:
                            raise Exception('{}: Duplicate {} "{}" on line {}'.format(
                                data_file, key, value, reader.line_num))
                        seen[key].add(value)

                if schema_file == 'extension-schema.json':
                    identifiers[id] = 0
                else:
                    # Ensure every version belongs to a known extension.
                    if id in identifiers:
                        identifiers[id] += 1
                    else:
                        raise Exception('{}: Id "{}" not in {}'.format(
                            os.path.basename(extension_versions_path), id, os.path.basename(extensions_path)))

    # Ensure every extension has at least one version.
    for id, count in identifiers.items():
        if not count:
            raise Exception('{}: Id "{}" not in {}'.format(
                os.path.basename(extensions_path), id, os.path.basename(extension_versions_path)))
