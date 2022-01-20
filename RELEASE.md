# How to Release

Here's a quick step-by-step checklist for making a new release of `pfx-brick-py`.

## Pre-release

1. update version in ``pfxbrick.__init__.py``

2. update version in ``doc/conf.py`` (two places!)

3. update CHANGELOG

4. create a release tag; e.g.
   ```
   $ git tag -a v0.7.0 -m 'version 0.7.0 release'
   ```

5. push the commits and tag to GitHub

6. confirm that CI tests pass on GitHub

7. under "tags" on GitHub, update the release notes

8. push the new release to PyPI:
   ```
   $ python setup.py sdist
   $ twine upload dist/*
   ```

9.  build the documentation:
   ```
   $ ./builddocs.sh
   ```

## Post-release

1. update version in ``pfxbrick.__version__`` to next version; e.g. '0.8.dev'

2. update version in ``doc/conf.py`` to the same (in two places)
