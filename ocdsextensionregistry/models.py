class ExtensionCSVModel:
    """Model representing details of the extension as raw values as they are presented in the CSV.

    This lets us do more validation."""

    def __init__(self, extension_id, repository_url, core, category):
        self.extension_id = extension_id
        self.repository_url = repository_url
        self.core = core
        self.category = category

    def get_extension_model(self):
        return ExtensionModel(
            repository_url=self.repository_url,
            core=self.core.strip().lower() == 'true',
            category=self.category
        )


class ExtensionModel:
    """Model representing an extension.

    Has cleaned values from both extension registry, and extension repository. Used for further work."""

    def __init__(self, repository_url, core, category):
        self.repository_url = repository_url
        self.core = core
        self.category = category
        self.extension_data = None
        self.git_tags = []
        self.extension_for_standard_versions = {}

    def get_git_clone_url(self):
        if self.repository_url[-1:] == '/':
            return self.repository_url[:-1] + '.git'
        else:
            return self.repository_url + '.git'

    def process(self, standard_versions):
        for ver in standard_versions:
            self.extension_for_standard_versions[ver] = ExtensionForStandardVersion(extension=self)
            if self.core:
                if 'v' + ver in self.git_tags:
                    self.extension_for_standard_versions[ver].git_reference = 'v' + ver
                else:
                    self.extension_for_standard_versions[ver].available = False
            elif 'compatibility' in self.extension_data:
                if does_any_version_in_list_match_version(self.extension_data['compatibility'], ver):
                    self.extension_for_standard_versions[ver].available = True
                else:
                    self.extension_for_standard_versions[ver].available = False


def does_any_version_in_list_match_version(check_list, version):
    version_bits = version.split('.')
    for check_version in check_list:
        check_version_bits = check_version.split('.')
        if check_version_bits[0] == version_bits[0] and check_version_bits[1] == version_bits[1]:
            return True
    return False


class ExtensionForStandardVersion:

    def __init__(self, extension):
        self.extension = extension
        self.available = True
        self.git_reference = 'master'

    def get_url_to_use_in_legacy_compiled_data(self):
        url_bits = self.extension.repository_url.split('/')
        url = 'https://raw.githubusercontent.com/' + url_bits[3] + '/' + url_bits[4] + '/' + \
              self.git_reference + '/'
        return url

    def get_url_to_use_in_standard_extensions_list(self):
        url_bits = self.extension.repository_url.split('/')
        url = 'https://raw.githubusercontent.com/' + url_bits[3] + '/' + url_bits[4] + '/' + \
              self.git_reference + '/extension.json'
        return url
