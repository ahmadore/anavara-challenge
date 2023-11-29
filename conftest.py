from glob import glob

old = "src/**/tests/fixtures/[!__]*.py"
new = "src/**/tests/fixtures.py"

pytest_plugins = [
    fixture_file.replace("/", ".").replace(".py", "")
    for fixture_file in glob(
        new,
        recursive=True
    )
]