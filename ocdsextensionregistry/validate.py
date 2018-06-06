import csv
import json
import os

from jsonschema import FormatChecker
from jsonschema.validators import Draft4Validator as validator


def validate_registry_csv(registry_csv_filename):
    ids = set()

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'extension-schema.json')) as f:
        schema = json.load(f)

    with open(registry_csv_filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            for error in validator(schema, format_checker=FormatChecker()).iter_errors(row):
                raise Exception('{}: {} ({})\n'.format(row['Id'], error.message, '/'.join(error.absolute_schema_path)))

            if row['Id'] in ids:
                raise Exception('Duplicate id "{}" on line {}'.format(row['Id'], reader.line_num))

            ids.add(row['Id'])
