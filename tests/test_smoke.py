from importlib.metadata import version

import project_name


def test_package_version():
    assert version("project-name") == project_name.__version__
