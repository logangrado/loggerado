.. loggerado documentation master file, created by
   sphinx-quickstart on Sun Feb 16 08:59:23 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

loggerado
=====================================

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   changelog
   api

Easily configure pretty python logs!

:func:`loggerado.configure_logger`

Example:

.. code-block:: python

   import logging
   import loggerado

   logger = logging.getLogger(__name__)

   loggerado.configure_logger(logger,'INFO')

   logger.info("Hello!")

.. code-block:: ansi

   [2001-01-01 00:00:00.000]     INFO | test_logger.logger: Hello!

You can also use `ansi=True` for colorized log messages.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
