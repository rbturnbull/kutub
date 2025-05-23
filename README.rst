=============
Kutub
=============

.. start-badges

|testing badge| |coverage badge| |docs badge| |black badge|

.. |testing badge| image:: https://github.com/rbturnbull/kutub/actions/workflows/testing.yml/badge.svg
    :target: https://github.com/rbturnbull/kutub/actions

.. |docs badge| image:: https://github.com/rbturnbull/kutub/actions/workflows/docs.yml/badge.svg
    :target: https://rbturnbull.github.io/kutub
    
.. |black badge| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    
.. |coverage badge| image:: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/rbturnbull/2b3790d81a696b1887aaceafff833d52/raw/coverage-badge.json
    :target: https://rbturnbull.github.io/kutub/coverage/
    
.. end-badges

.. start-quickstart

A Django app to create an inventory of manuscript descriptions.

Installation
==================================

Install using pip:

.. code-block:: bash

    pip install git+https://github.com/rbturnbull/kutub.git

Configuration
==================================

Add ``kutub`` to your ``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        "watson",
        "reversion",
        "sekizai",
        "widget_tweaks",
        "django_select2",
        "publications",
        "kutub",
    ]

Add the following to your ``urls.py``:

.. code-block:: python

    urlpatterns = [
        ...
        path("select2/", include("django_select2.urls")),
        path("publications/", include("publications.urls")),
        path("kutub/", include("kutub.urls")),
    ]


.. end-quickstart



Credits 
==================================

.. start-credits

- Robert Turnbull (Melbourne Data Analytics Platform, University of Melbourne)

.. end-credits