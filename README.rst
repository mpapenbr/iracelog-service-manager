========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/iracelog-service-manager/badge/?style=flat
    :target: https://iracelog-service-manager.readthedocs.io/
    :alt: Documentation Status

.. |codecov| image:: https://codecov.io/gh/mpapenbr/iracelog-service-manager/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://codecov.io/github/mpapenbr/iracelog-service-manager

.. |version| image:: https://img.shields.io/pypi/v/iracelog-service-manager.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/iracelog-service-manager

.. |wheel| image:: https://img.shields.io/pypi/wheel/iracelog-service-manager.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/iracelog-service-manager

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/iracelog-service-manager.svg
    :alt: Supported versions
    :target: https://pypi.org/project/iracelog-service-manager

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/iracelog-service-manager.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/iracelog-service-manager

.. |commits-since| image:: https://img.shields.io/github/commits-since/mpapenbr/iracelog-service-manager/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/mpapenbr/iracelog-service-manager/compare/v0.0.0...main



.. end-badges

An example package. Generated with cookiecutter-pylibrary.

* Free software: Apache Software License 2.0

Installation
============

::

    pip install iracelog-service-manager

You can also install the in-development version with::

    pip install https://github.com/mpapenbr/iracelog-service-manager/archive/main.zip


Documentation
=============


https://iracelog-service-manager.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
