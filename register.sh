# Convert the Markdown README that's Github's bread and butter
# to PyPI's preferred reStructuredTxt using pandoc.

pandoc --from=markdown_github --to=rst --output=README.rst README.md

python setup.py register -r pypi

# TODO: Confirm upload...

python setup.py sdist upload -r pypi

rm README.rst
