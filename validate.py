import ocdsextensionregistry.validate
import os

if __name__ == "__main__":
    ocdsextensionregistry.validate.registry_csv_filename = \
        os.path.dirname(os.path.abspath(__file__)) + '/extensions.csv'
    ocdsextensionregistry.validate.validate_registry_csv()
