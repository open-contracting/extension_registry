import ocdsextensionregistry.models


def test_parse_core_true():
    csv_model = ocdsextensionregistry.models.ExtensionCSVModel(
        extension_id="test",
        repository_url="https://github.com/open-contracting/ocds_documentation_extension",
        core="True",
        category="contract"
    )
    model = csv_model.get_extension_model()
    assert model.core is True


def test_parse_core_false():
    csv_model = ocdsextensionregistry.models.ExtensionCSVModel(
        extension_id="test",
        repository_url="https://github.com/open-contracting/ocds_documentation_extension",
        core="False",
        category="contract"
    )
    model = csv_model.get_extension_model()
    assert model.core is False
