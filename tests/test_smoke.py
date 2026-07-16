def test_import():
    import project_name  # noqa: F401

    assert project_name is not None
