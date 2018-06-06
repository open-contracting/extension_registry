import ocdsextensionregistry.compile
import os


if __name__ == "__main__":
    ocdsextensionregistry.compile.registry_csv_filename = \
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extensions.csv')

    ocdsextensionregistry.compile.registry_categories_csv_filename = \
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'categories.csv')

    ocdsextensionregistry.compile.extensions_repositories_folder = \
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "extensions_repositories")
    if not os.path.isdir(ocdsextensionregistry.compile.extensions_repositories_folder):
        os.makedirs(ocdsextensionregistry.compile.extensions_repositories_folder)

    ocdsextensionregistry.compile.legacy_output_folder = \
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "legacy_output")
    if not os.path.isdir(ocdsextensionregistry.compile.legacy_output_folder):
        os.makedirs(ocdsextensionregistry.compile.legacy_output_folder)

    ocdsextensionregistry.compile.compile_registry()
