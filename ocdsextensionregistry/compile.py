import csv
from .models import ExtensionModel
import os
import subprocess
import datetime
import json

standard_versions = ['1.0.3', '1.1.1', '1.1.3']


def compile_registry(registry_csv_filename, extensions_repositories_folder, legacy_output_folder):
    if registry_csv_filename is None:
        raise Exception("Please set registry_csv_filename")
    if extensions_repositories_folder is None:
        raise Exception("Please set extensions_repositories_folder")
    os.makedirs(extensions_repositories_folder, exist_ok=True)
    extensions = _load_data(registry_csv_filename)
    _fetch_extensions(extensions, extensions_repositories_folder)
    _load_extension_data(extensions, extensions_repositories_folder)
    _process_data(extensions)
    if legacy_output_folder is not None:
        os.makedirs(legacy_output_folder, exist_ok=True)
        _make_legacy_output(extensions, legacy_output_folder)


def _load_data(registry_csv_filename):
    extensions = {}

    with open(registry_csv_filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            extensions[row['Id']] = ExtensionModel(
                repository_url=row['RepositoryURL'],
                category=row['Category'],
                core=row['Core'] == 'True',
            )

    return extensions


def _fetch_extensions(extensions, extensions_repositories_folder):
    for extension_id, data in extensions.items():
        folder = os.path.join(extensions_repositories_folder,  extension_id)
        if os.path.isdir(folder):
            command = "git pull origin master"
            subprocess.check_call(command, shell=True, cwd=folder)
        else:
            # we are trusting the model to validate git clone url is a real url and not a security problem!
            command = "git clone " + data.get_git_clone_url() + '  ' + folder
            subprocess.check_call(command, shell=True)


def _load_extension_data(extensions, extensions_repositories_folder):
    for extension_id in extensions.keys():
        # Load the master json
        with open(os.path.join(extensions_repositories_folder,  extension_id, 'extension.json')) as fp:
            extensions[extension_id].extension_data = json.load(fp)
        # Load list of tags
        results = subprocess.check_output(
            "git tag",
            cwd=os.path.join(extensions_repositories_folder, extension_id),
            shell=True
        )
        extensions[extension_id].git_tags = results.decode("utf-8") .split('\n')


def _process_data(extensions):
    for extension_id in extensions.keys():
        extensions[extension_id].process(standard_versions=standard_versions)


def _make_legacy_output(extensions, legacy_output_folder):
    for ver in standard_versions:
        out = {
            "last_updated": str(datetime.datetime.utcnow()),
            "extensions": []
        }

        for extension_id, extension in extensions.items():
            if extension.extension_for_standard_versions[ver].available:
                out_extension = {
                    'slug': extension_id,
                    "category": extension.category,
                    "documentationUrl": {
                        "en": extension.extension_data["documentationUrl"]["en"]
                    },
                    "name": {
                        "en": extension.extension_data["name"]["en"]
                    },
                    "core": extension.core,
                    "url": extension.extension_for_standard_versions[ver].get_url_to_use_in_legacy_compiled_data(),
                    "description": {
                        "en": extension.extension_data["description"]["en"]
                    },
                    "documentation_url": extension.extension_data["documentationUrl"]["en"]
                }
                out['extensions'].append(out_extension)

        full_json = json.dumps(out, sort_keys=True, indent=4)
        with open(os.path.join(legacy_output_folder, 'legacy-extensions.'+ver+'.json'), 'w') as jsonfile:
            jsonfile.write(full_json)
        with open(os.path.join(legacy_output_folder, 'legacy-extensions.'+ver+'.js'), 'w') as jsonfile:
            jsonfile.write("extensions_callback(" + full_json + ")")
