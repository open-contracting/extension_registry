# Extension Registry

This repository contains the two authoritative tables (CSV files) that list the registered [OCDS extensions](https://standard.open-contracting.org/latest/en/extensions/):

* [`extensions.csv`](/extensions.csv) lists the extensions in the registry
* [`extension_versions.csv`](/extension_versions.csv) lists each version of each extension in the registry

## How to register an extension

### Adding a new extension

[Create an issue](https://github.com/open-contracting/extension_registry/issues/new) with a link to your extension. The registry's maintainers will evaluate its quality and relevance and provide feedback in the created issue or in the extension's repository. When appropriate, the maintainers will update the registry and close the issue.

### Adding a new version of an extension

Create an issue or pull request about updating `extension_versions.csv`. See below on how to edit this file.

## How to edit the CSV files

### [`extensions.csv`](/extensions.csv)

This file has one extension per row. The row order has no effect, but alphabetical order is maintained for easier scanning and change tracking.

The CSV columns are:

* `Id` (required): A unique identifier for the extension, composed of underscores and lowercase and uppercase ASCII letters. If the extension follows the [repository name guidance](https://extensions.open-contracting.org/en/publishers/#repository-name), this `Id` can be the repository name without the `ocds_` prefix and `_extension` suffix.
*  `Category`: The [standard documentation](https://standard.open-contracting.org/) lists, in specific locations, extensions that target a specific part of the schema. Extensions may set a [category](https://github.com/open-contracting/standard-maintenance-scripts/blob/main/schema/extension-schema.json) to appear in one of these lists.
*  `Core`: The standard documentation defines [core extensions](https://standard.open-contracting.org/latest/en/extensions/), and the standard's [governance process](https://standard.open-contracting.org/latest/en/support/governance/) determines whether an extension is core.

### [`extension_versions.csv`](/extension_versions.csv)

This file has one version (or release) of an extension per row. The row order has no effect, but alphabetical order is maintained for easier scanning and change tracking.

A version of an extension can be either 'live' or 'frozen'. A live version is continuously updated at the same URL; for example, an author publishes an extension on GitHub, and continuously updates the default branch. A frozen version is published once at a given URL and never updated; for example, an author tags a commit and releases that version of the extension. An extension can have both live and frozen versions. An extension ought to have only one live version.

The CSV columns are:

* `Id` (required): An `Id` from `extensions.csv`.
* `Date`:
  * If the extension is *frozen*, this is the date of the release (e.g. as shown on the extension's releases page on GitHub), or the date on which the row was inserted.
  * If the extension is *live*, this is blank.
* `Version` (required):
  * If the extension is *frozen*, this is the tag of the release (e.g. as shown on the extension's releases page on GitHub), or a version number chosen by the extension's author.
  * If the extension is *live*, this is the branch name at which the version is continuously updated, or a version name chosen by the extension's author.
* `Base URL` (required): The URL to which `extension.json` can be appended to retrieve the metadata for this version of the extension.
* `Download URL`: The URL to retrieve a ZIP archive of this version of the extension.

## Maintenance

Install dependencies:

```bash
pip install -r requirements_dev.txt
```

To add a new extension to `extensions.csv` and `extension_versions.csv`, run, for example:

```bash
./manage.py add https://github.com/org/repo
```

To check for new versions of registered extensions, run:

```bash
./manage.py refresh
```

The standard documentation renders lists of community extensions using an `extensions.json` file, that aggregates information from the registry and each extension. This file is published at [build/extensions.json](/build/extensions.json). To regenerate the file:

```bash
./manage.py build
```

This repository has tests to validate `extensions.csv` and `extension_versions.csv` and to check the integrity of `extensions.json`.
