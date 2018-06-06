import ocdsextensionregistry.validate
import os
import pytest


def test_ok():
    ocdsextensionregistry.validate.validate_registry_csv(os.path.dirname(__file__) + '/validate_ok.csv')


def test_dupe_id():
    with pytest.raises(Exception) as excinfo:
        ocdsextensionregistry.validate.validate_registry_csv(os.path.dirname(__file__) + '/validate_dupe_id.csv')
    assert 'Duplicate id "signatories" on line 3' in str(excinfo.value)


def test_no_category():
    with pytest.raises(Exception) as excinfo:
        ocdsextensionregistry.validate.validate_registry_csv(os.path.dirname(__file__) + '/validate_no_category.csv')
    assert '\'\' is not one of ' in str(excinfo.value)


def test_bad_category():
    with pytest.raises(Exception) as excinfo:
        ocdsextensionregistry.validate.validate_registry_csv(os.path.dirname(__file__) + '/validate_bad_category.csv')
    assert '\'contractCategoryDoesNotExistThisIsNotAStandardCategory\' is not one of ' in str(excinfo.value)


def test_no_core():
    with pytest.raises(Exception) as excinfo:
        ocdsextensionregistry.validate.validate_registry_csv(os.path.dirname(__file__) + '/validate_no_core.csv')
    assert '\'\' is not one of' in str(excinfo.value)


def test_bad_core1():
    with pytest.raises(Exception) as excinfo:
        ocdsextensionregistry.validate.validate_registry_csv(os.path.dirname(__file__) + '/validate_bad_core1.csv')
    assert '\'cats\' is not one of ' in str(excinfo.value)


def test_bad_core2():
    with pytest.raises(Exception) as excinfo:
        ocdsextensionregistry.validate.validate_registry_csv(os.path.dirname(__file__) + '/validate_bad_core2.csv')
    assert '\'true\' is not one of ' in str(excinfo.value)


def test_bad_id_space():
    with pytest.raises(Exception) as excinfo:
        ocdsextensionregistry.validate.validate_registry_csv(os.path.dirname(__file__) + '/validate_bad_id_space.csv')
    assert '\'haz signatories\' does not match' in str(excinfo.value)


def test_bad_id_questionmark():
    with pytest.raises(Exception) as excinfo:
        ocdsextensionregistry.validate.validate_registry_csv(os.path.dirname(__file__) + '/validate_bad_id_questionmark.csv')
    assert '\'signatories?\' does not match' in str(excinfo.value)
