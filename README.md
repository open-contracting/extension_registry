# Extension Registry

This repository contains the two authoritative tables (CSV files) that list the registered core and community [OCDS extensions](http://standard.open-contracting.org/latest/en/extensions/).

## How to register an extension

### Adding a new extension

[Create an issue](https://github.com/open-contracting/extension_registry/issues/new) with a link to your extension. The registry's maintainers will evaluate the extension's quality and relevance and provide feedback in the issue or the extension's repository. If appropriate, the maintainers will insert a row, in alphabetical order, in each of `extensions.csv` and `extension_versions.csv`.

### Adding a new version of an extension

Create an issue, or a pull request if able, about inserting a row in `extension_versions.csv`. See the documentation below regarding the usage of each column of `extension_versions.csv`.

## Table schema

### `extensions.csv`

This file has one extension per row. The row order has no effect, but alphabetical order is maintained for easier scanning and change tracking.

The CSV columns are:

* `Id` (required): A unique identifier for the extension, composed of underscores and lowercase and uppercase ASCII letters. If the extension follows the [extension naming guidance](https://github.com/open-contracting/standard_extension_template#naming-extension-repositories), this `Id` can be the extension repository's name, without the `ocds_` prefix and `_extension` suffix.
*  `Category`: The [standard documentation](http://standard.open-contracting.org/) lists, in specific locations, extensions that target a specific part of the schema. Extensions may set a [category](/schema/extensions-schema.json) to appear in one of these lists.
*  `Core`: The standard documentation defines [core extensions](http://standard.open-contracting.org/latest/en/extensions/), and the standard's [governance process](http://standard.open-contracting.org/latest/en/support/governance/) determines whether an extension is core.

### `extension_versions.csv`

This file has one version (or release) of an extension per row. The row order has no effect, but alphabetical order is maintained for easier scanning and change tracking.

A version of an extension can be either 'live' or 'frozen'. A live version is continously updated at the same URL; for example, an author publishes an extension on GitHub, and continously updates the default branch. A frozen version is published once at a given URL and never updated; for example, an author tags a commit and releases that version of the extension. An extension can have both live and frozen versions. An extension ought to have only one live version.

The CSV columns are:

* `Id` (required): An `Id` from `extensions.csv`.
* `Date`:
  * If the extension is *frozen*, set this to the date of the release (e.g. as shown on the extension's releases page on GitHub), or the date on which the row was inserted.
  * If the extension is *live*, leave this blank.
* `Version` (required):
  * If the extension is *frozen*, set this to the tag of the release (e.g. as shown on the extension's releases page on GitHub), or a version number chosen by the extension's author.
  * If the extension is *live*, set this to the branch name at which the version is continuously updated, or to a version name chosen by the extension's author.
* `Base URL` (required): The URL to which `extension.json` can be appended to retrieve the metadata for this version of the extension.
* `Download URL`: The URL to retrieve a ZIP archive of this version of the extension.
