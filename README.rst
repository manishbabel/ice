========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/ice/badge/?style=flat
    :target: https://readthedocs.org/projects/ice
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/manishbabel/ice.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/manishbabel/ice

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/manishbabel/ice?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/manishbabel/ice

.. |version| image:: https://img.shields.io/pypi/v/ice.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/ice

.. |commits-since| image:: https://img.shields.io/github/commits-since/manishbabel/ice/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/manishbabel/ice/compare/v0.0.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/ice.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/ice

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/ice.svg
    :alt: Supported versions
    :target: https://pypi.org/project/ice

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/ice.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/ice


.. end-badges

Integration Control Engine

* Free software: MIT license

Installation
============

::

    pip install ice

Documentation
=============


https://ice.readthedocs.io/


Development
===========

To run the all tests run::

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
