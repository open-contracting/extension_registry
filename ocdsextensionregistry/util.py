import csv


def load_categories_from_csv(registry_categories_csv_filename):
    categories = []
    with open(registry_categories_csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        reader.__next__()  # Throw away the heading line
        for row in reader:
            # To decide if row has any data in, check it has value.
            if len(row) > 0:
                category = row[0].strip()
                if category:
                    if category in categories:
                        raise Exception("Category %s is already registered! (Duplicate is on line %d)" % (
                            category, reader.line_num))
                    categories.append(category)
    return categories
