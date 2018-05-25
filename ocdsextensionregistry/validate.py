import csv
from .models import ExtensionCSVModel

registry_csv_filename = None


def validate_registry_csv():
    extensions = {}
    with open(registry_csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        reader.__next__() # Throw away the heading line
        for row in reader:
            # To decide if row has any data in, check it has values and it has an id.
            if len(row) > 0:
                extension_id = row[0].lower().strip()
                if extension_id:
                    if extension_id in extensions.keys():
                        raise Exception("Extension %s is already registered! (Duplicate is on line %d)" % (extension_id, reader.line_num ))
                    extension_csv_model = ExtensionCSVModel(
                        extension_id=row[0],
                        repository_url=row[1],
                        category=row[2],
                        core=row[3]
                    )
                    extension_csv_model.validate()
                    extensions[extension_id] = extension_csv_model
