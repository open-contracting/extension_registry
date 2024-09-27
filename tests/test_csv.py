import csv
import os
from collections import defaultdict
from typing import Literal

import requests
from pydantic import AnyUrl, BaseModel, ConfigDict, Field, ValidationError


class Extension(BaseModel):
    model_config = ConfigDict(extra="forbid")

    Id: str = Field(pattern=r"^[A-Za-z_]+$")
    Category: (
        Literal[
            "amendment",
            "award",
            "bids",
            "budget",
            "contract",
            "document",
            "implementation",
            "item",
            "milestones",
            "package",
            "parties",
            "partyDetail",
            "planning",
            "release",
            "tender",
            "transaction",
        ]
        | None
    ) = None
    Core: Literal["true"] | None = None


class ExtensionVersion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    Id: str = Field(pattern=r"^[a-zA-Z_]+$")
    Date: str | None = Field(None, pattern=r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
    Version: str = Field(min_length=1)
    Base_URL: AnyUrl = Field(alias="Base URL")
    Download_URL: AnyUrl | None = Field(None, alias="Download URL")


def test_registry():
    # Keep track of extension identifiers, to ensure consistency across files.
    identifiers = {}

    for filename, model, uniqueness in (
        # Id must be unique in extensions.csv.
        ("extensions.csv", Extension, {"Id": None}),
        # Version and Base URL must be unique, within the scope of a given Id, in extension_versions.csv.
        ("extension_versions.csv", ExtensionVersion, {"Version": "Id", "Base URL": "Id"}),
    ):
        # Count the occurrences of a key-value pair, within a given scope.
        seen = {}
        for key, scope in uniqueness.items():
            if scope:
                seen[scope] = defaultdict(lambda: defaultdict(set))
            else:
                seen[key] = set()

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", filename)) as f:
            reader = csv.DictReader(f)
            for row in reader:
                extension_id = row["Id"]

                for key in reader.fieldnames:
                    if not row[key]:
                        del row[key]

                try:
                    model.model_validate_strings(row, strict=True)
                except ValidationError as e:
                    raise AssertionError(f"{row}\n{e}") from None

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
                                f'{filename}: Duplicate {key} "{value}" on line {reader.line_num} '
                                f'in scope of {scope} "{row[scope]}"'
                            )
                        seen[scope][row[scope]][key].add(value)
                    else:
                        if value in seen[key]:
                            raise AssertionError(f'{filename}: Duplicate {key} "{value}" on line {reader.line_num}')
                        seen[key].add(value)

                if filename == "extensions.csv":
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
