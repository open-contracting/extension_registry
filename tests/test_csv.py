import csv
import json
import os
from collections import defaultdict

import requests
from jsonschema import FormatChecker
from jsonschema.validators import Draft4Validator as Validator


def test_registry():
    configuration = {
        # Id must be unique in extensions.csv.
        "extensions.csv": {"Id": None},
        # Version and Base URL must be unique, within the scope of a given Id, in extension_versions.csv.
        "extension_versions.csv": {"Version": "Id", "Base URL": "Id"},
    }

    # Keep track of extension identifiers, to ensure consistency across files.
    identifiers = {}

    for csv_name, uniqueness in configuration.items():
        schema_name = f"{os.path.splitext(csv_name)[0]}-schema.json"

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "schema", schema_name)) as f:
            schema = json.load(f)

        # Count the occurrences of a key-value pair, within a given scope.
        seen = {}
        for key, scope in uniqueness.items():
            if scope:
                seen[scope] = defaultdict(lambda: defaultdict(set))
            else:
                seen[key] = set()

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", csv_name)) as f:
            reader = csv.DictReader(f)
            for row in reader:
                extension_id = row["Id"]

                for key in reader.fieldnames:
                    if not row[key]:
                        del row[key]

                for error in Validator(schema, format_checker=FormatChecker()).iter_errors(row):
                    raise AssertionError(f"{extension_id}: {error.message} ({'/'.join(error.absolute_schema_path)})\n")

                # Validate that URLs resolve.
                if row.get("Base URL"):
                    response = requests.get(row["Base URL"] + "extension.json", timeout=10)
                    response.raise_for_status()
                if row.get("Download URL"):
                    response = requests.get(row["Download URL"], timeout=10)
                    response.raise_for_status()

                # Validate the uniqueness of a key-value pair, within a given scope.
                for key, scope in uniqueness.items():
                    value = row[key]
                    if scope:
                        if value in seen[scope][row[scope]][key]:
                            raise AssertionError(
                                f'{csv_name}: Duplicate {key} "{value}" on line {reader.line_num} '
                                f'in scope of {scope} "{row[scope]}"'
                            )
                        seen[scope][row[scope]][key].add(value)
                    else:
                        if value in seen[key]:
                            raise AssertionError(f'{csv_name}: Duplicate {key} "{value}" on line {reader.line_num}')
                        seen[key].add(value)

                if csv_name == "extensions.csv":
                    identifiers[extension_id] = 0
                # Ensure every version belongs to a known extension.
                elif extension_id in identifiers:
                    identifiers[extension_id] += 1
                else:
                    raise AssertionError(f'extension_versions.csv: Id "{extension_id}" not in extensions.csv')

    # Ensure every extension has at least one version.
    for extension_id, count in identifiers.items():
        if not count:
            raise AssertionError(f'extensions.csv: Id "{extension_id}" not in extension_versions.csv')
