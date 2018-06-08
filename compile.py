import ocdsextensionregistry.compile
import os


if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    ocdsextensionregistry.compile.compile_registry(
        registry_csv_filename=os.path.join(directory, 'extensions.csv'),
        extensions_repositories_folder=os.path.join(directory, 'extensions_repositories'),
        legacy_output_folder=os.path.join(directory, 'legacy_output'),
    )
