# Extension Repository

The place where extensions can be registered in order to appear in the docs.

Each extension lives in its own directory in this repo and must contain an _entry.json_ file following the format described in the schema file _entry-schema.json_.

_entry.json_ must validate against the schema before being included in the registry.

## entry.json

A list of entries for this extension. Multiple versions of the same extensions can be registered, the first being the default version.

### Required fields for each entry

* `category`: part of the docs the extensions appears in.
* `core`: a boolean declaring the extension core (true) or community (false).
* `description`: description of the extension, an object mapping language codes to the description of the extension in the language.
* `documentationUrl`: documentation URL for the extension, an object mapping language codes to an URL with documentation in the language.
* `name`: name of the extension, an object mapping language codes to the name of the extension in the language
* `url`: URL of the extension repository, pointing at an _extension.json_ file.

### Optional fields

* `dependencies`: a list of other extensions that this extension depends on.
* `compatibility`: a list of versions of OCDS schema versions this extension is valid against.
* `version`: an optional semver of the extension.
* `slug`: indicates where the extension documentation lives in the standard docs, i.e. a "location" slug means the docs are at `http://standard.open-contracting.org/*version*/*lang*/extensions/location` ── applies to core extensions only.

Here is an example `entry.json`:

```json
[{
  "name": {
    "en" : "Example Extension",
    "es" : "Ejemplo de Extensión"
  },
  "description": {
    "en": "Example Extension",
    "es": "Ejemplo de Extensión"
  },
  "url": "http://www.example.com/extension/extension.json",
  "documentationUrl": {
    "en": "http://www.example.com/extension_documentation/en_docs",
    "es": "http://www.example.com/extension_documentation/es_docs"
  },
  "category": "item",
  "core": false,
  "slug": "example",
  "dependencies": ["path/to/extension1/extension.json","path/to/extension2/extension.json" ]
}]
```

## Maintenance

Install dependencies:

    pip install -r requirements.txt

Compile entries:

    python compile.py

The _compile.py_ script will generate two non-version-controlled files, **_extensions.json_** and **_extensions.js_**, which are the reference files that OCDS needs to build the documentation on extensions.
