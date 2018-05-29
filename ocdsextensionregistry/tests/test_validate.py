import ocdsextensionregistry.validate
import os
import pytest


def test_ok():
    ocdsextensionregistry.validate.registry_csv_filename = os.path.dirname(__file__) + '/validate_ok.csv'
    ocdsextensionregistry.validate.registry_categories_csv_filename = \
        os.path.dirname(__file__) + '/standard_categories.csv'
    ocdsextensionregistry.validate.validate_registry_csv()


def test_only_github():
    ocdsextensionregistry.validate.registry_csv_filename = os.path.dirname(__file__) + '/validate_only_github.csv'
    ocdsextensionregistry.validate.registry_categories_csv_filename = \
        os.path.dirname(__file__) + '/standard_categories.csv'
    with pytest.raises(Exception) as excinfo:
        ocdsextensionregistry.validate.validate_registry_csv()
    assert 'Repository must be on GitHub' in str(excinfo.value)


def test_dupe_id():
    ocdsextensionregistry.validate.registry_csv_filename = os.path.dirname(__file__) + '/validate_dupe_id.csv'
    ocdsextensionregistry.validate.registry_categories_csv_filename = \
        os.path.dirname(__file__) + '/standard_categories.csv'
    with pytest.raises(Exception) as excinfo:
        ocdsextensionregistry.validate.validate_registry_csv()
    assert 'Extension signatories is already registered! (Duplicate is on line 3)' in str(excinfo.value)


def test_no_category():
    ocdsextensionregistry.validate.registry_csv_filename = os.path.dirname(__file__) + '/validate_no_category.csv'
    ocdsextensionregistry.validate.registry_categories_csv_filename = \
        os.path.dirname(__file__) + '/standard_categories.csv'
    with pytest.raises(Exception) as excinfo:
        ocdsextensionregistry.validate.validate_registry_csv()
    assert '\'\' is not one of ' in str(excinfo.value)


def test_bad_category():
    ocdsextensionregistry.validate.registry_csv_filename = os.path.dirname(__file__) + '/validate_bad_category.csv'
    ocdsextensionregistry.validate.registry_categories_csv_filename = \
        os.path.dirname(__file__) + '/standard_categories.csv'
    with pytest.raises(Exception) as excinfo:
        ocdsextensionregistry.validate.validate_registry_csv()
    assert '\'contractCategoryDoesNotExistThisIsNotAStandardCategory\' is not one of ' in str(excinfo.value)


def test_no_core():
    ocdsextensionregistry.validate.registry_csv_filename = os.path.dirname(__file__) + '/validate_no_core.csv'
    ocdsextensionregistry.validate.registry_categories_csv_filename = \
        os.path.dirname(__file__) + '/standard_categories.csv'
    with pytest.raises(Exception) as excinfo:
        ocdsextensionregistry.validate.validate_registry_csv()
    assert '\'\' is not one of' in str(excinfo.value)


def test_bad_core():
    ocdsextensionregistry.validate.registry_csv_filename = os.path.dirname(__file__) + '/validate_bad_core.csv'
    ocdsextensionregistry.validate.registry_categories_csv_filename = \
        os.path.dirname(__file__) + '/standard_categories.csv'
    with pytest.raises(Exception) as excinfo:
        ocdsextensionregistry.validate.validate_registry_csv()
    assert '\'cats\' is not one of ' in str(excinfo.value)


def test_bad_id_space():
    ocdsextensionregistry.validate.registry_csv_filename = os.path.dirname(__file__) + '/validate_bad_id_space.csv'
    ocdsextensionregistry.validate.registry_categories_csv_filename = \
        os.path.dirname(__file__) + '/standard_categories.csv'
    with pytest.raises(Exception) as excinfo:
        ocdsextensionregistry.validate.validate_registry_csv()
    assert '\'haz signatories\' does not match' in str(excinfo.value)


def test_bad_id_questionmark():
    ocdsextensionregistry.validate.registry_csv_filename = os.path.dirname(__file__) + '/validate_bad_id_questionmark.csv'
    ocdsextensionregistry.validate.registry_categories_csv_filename = \
        os.path.dirname(__file__) + '/standard_categories.csv'
    with pytest.raises(Exception) as excinfo:
        ocdsextensionregistry.validate.validate_registry_csv()
    assert '\'signatories?\' does not match' in str(excinfo.value)
