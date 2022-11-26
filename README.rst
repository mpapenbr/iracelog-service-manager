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

.. |docs| image:: https://readthedocs.org/projects/iracelog-service-manager/badge/?style=flat
    :target: https://iracelog-service-manager.readthedocs.io/
    :alt: Documentation Status

.. |codecov| image:: https://codecov.io/gh/mpapenbr/iracelog-service-manager/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://codecov.io/github/mpapenbr/iracelog-service-manager


.. |commits-since| image:: https://img.shields.io/github/commits-since/mpapenbr/iracelog-service-manager/v0.5.0.svg
    :alt: Commits since latest release
    :target: https://github.com/mpapenbr/iracelog-service-manager/compare/v0.5.0...main



.. end-badges

This module is the backend for processing WAMP messages in the iRacelog project.

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

Database
--------

The connection to the database is configured via the environment variable `DB_URL`. 

::

    DB_URL=postgresql://<user>:<password>@<dbhost>/<db_schema>

.. Note::

    When using the tox environment the env var TEST_DB_URL is used for DB_URL

Tests
~~~~~

For local developer tests the developer is responsible for managing the test instance. 
To start with, create an empty database, define the `TEST_DB_URL` and initialize the database via `tox -e alembic`

::

    export TEST_DB_URL=postgresql://test:secret@localhost:5432/iracelog_test
    tox -e alembic

When running tests locally you will need to export the above db connection with the key TEST_DB_URL. 
To get all vars in .env exposed to the shell use
::
    
    export $(cat .env)


Images
~~~~~~

There is an experimental Dockerfile-small-img. 
The main idea is to have a single statically linked executable in an otherwise empty image.
Drawbacks:

- We cannot use the scratch base image since the Python Click module requires locales to be available. 
- While the single executable would be fine for archiver and manager we would need another image for the db migration via alembic. 

So for now we continue to work with the (big) python image.

This is based on this article https://medium.com/analytics-vidhya/dockerizing-a-rest-api-in-python-less-than-9-mb-and-based-on-scratch-image-ef0ee3ad3f0a