# Extension Repository

The place where extensions can be registered in order to appear in the docs.

## The data files in this repository

Edit the extensions.csv file to add an extension. One row per extension. The order of rows is not important. Columns are:

  *  Id - this should be unique and contain alphanumeric or underscore characters only.
  *  RepositoryURL - GitHub repository front page. eg "https://github.com/open-contracting/ocds_contract_signatories_extension".
     Direct links to an extension.json file should not be included.
  *  Category - one value, a string.
  *  Core - a boolean value, "true" or "false".


(Currently RepositoryURL only supports GitHub. If you want to use GitLab, Bitbucket or another alternative that should
be fine but you need to open an issue first as some minor work to support that will be needed.)


## Maintenance

Install dependencies:

    pip install -r requirements.txt

Validate entries:

    python validate.py

Compile entries:

    python compile.py

The _compile.py_ script will generate non-version-controlled files in the folders "output" and "legacy_output".

To do this, it will need to check out each extension repository. (The "git" command should be available). It will do this in the "extensions_repositories" folder.

pytest tests are available in ocdsextensionregistry/tests.

