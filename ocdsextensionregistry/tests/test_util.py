from ocdsextensionregistry.util import string_to_boolean


def test_string_to_boolean_1():
    assert string_to_boolean('true') is True


def test_string_to_boolean_2():
    assert string_to_boolean(' TRue') is True


def test_string_to_boolean_3():
    assert string_to_boolean(' False') is False
