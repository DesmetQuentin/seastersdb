.. _sql:

SQL queries in SEASTERS
=======================

Generalities
------------

You may have noticed it during :ref:`installation <install-main>`: seastersdb is
essentially based on `DuckDB <duckdb.org>`_, which provides a friendly SQL interface
to store and retrieve data in and from a relational database. With seastersdb, we
only provide a tool for the "data retrieval" part. SQL (Structured Query Language) is a
quite intuitive language allowing quick search and filtering, querying efficiently the
database's tables of rows (records) and columns (fields). This documentation does not
include a course on SQL queries; we only provide our database-specific macros, together
with a number of examples. If you need further information on the syntax, we recommend
having a look at the "Query Syntax" section of
`this documentation <https://duckdb.org/docs/stable/sql/query_syntax/select>`_.


.. _macros:

SEASTERS macros & functions
---------------------------

Beyond leveraging DuckDB, seastersdb provides SQL macros and functions to enhance the
user experience while querying the SEASTERS database.


Macros
~~~~~~

Although there are a few exceptions, SEASTERS macros are built as follows (replace
``<network>`` by one among ``bsrn``, ``ghcnd``, ``ghcnh`` and ``gsdr``):

- ``<network>()`` points to the actual data records;
- ``<network>_var()`` points to the variable metadata;
- ``<network>_inv()`` points to the inventory (available time interval by station);
- ``<network>_stations()`` points to the station metadata.

Exceptions are:

- BSRN data records are actually divided in disctinct datasets with specific
  inventories and variables, such that ``bsrn()`` actually takes a ``dataset`` argument
  among ``'radiosonde'``, ``'radiation_10m'``, ``'radiation'`` and ``'SYNOP'``.
- ``gsdr_var()`` does not exist, because this network only includes precipitation data in
  millimeter, with no more variable metadata.


The table below lists all resulting macros with their specific descriptions:

.. list-table::
   :header-rows: 1

   * - Name
     - Description
   * - ``bsrn(dataset)``
     - Access BSRN observational data for a given dataset. Allowed values
       for ``dataset`` are: ``'radiosonde'``, ``'radiation_10m'``,
       ``'radiation'``, and ``'SYNOP'``.
   * - ``bsrn_stations()``
     - Access station metadata for the BSRN network.
   * - ``bsrn_inv()``
     - Access inventory for the BSRN network.
   * - ``bsrn_var()``
     - Access variable metadata for the BSRN network.
   * - ``ghcnd()``
     - Access observational data for the GHCNd network.
   * - ``ghcnd_stations()``
     - Access station metadata for the GHCNd network.
   * - ``ghcnd_inv()``
     - Access inventory for the GHCNd network.
   * - ``ghcnd_var()``
     - Access variable metadata for the GHCNd network.
   * - ``ghcnh()``
     - Access observational data for the GHCNh network.
   * - ``ghcnh_stations()``
     - Access station metadata for the GHCNh network.
   * - ``ghcnh_inv()``
     - Access inventory for the GHCNh network.
   * - ``ghcnh_var()``
     - Access variable metadata for the GHCNh network.
   * - ``gsdr()``
     - Access observational data for the GSDR network.
   * - ``gsdr_stations()``
     - Access station metadata for the GSDR network.
   * - ``gsdr_inv()``
     - Access inventory for the GSDR network.


SEASTERS relational schemas
~~~~~~~~~~~~~~~~~~~~~~~~~~~


Tables behind SEASTERS macros are linked to each other following the relational schemas
shown below. They can be joint using the primary keys emphasized in bold.

.. tab-set::

   .. tab-item:: GHCNd

      .. image:: ../_static/schema_ghcnd.webp
         :alt: GHCNd relational schema
         

   .. tab-item:: GHCNh

      .. image:: ../_static/schema_ghcnh.webp
         :alt: GHCNh relational schema
         

   .. tab-item:: GSDR

      .. image:: ../_static/schema_gsdr.webp
         :alt: GSDR relational schema
         

   .. tab-item:: BSRN
   
      .. image:: ../_static/schema_bsrn.webp
         :alt: BSRN relational schema


Functions
~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Name
     - Description
   * - ``overlaps(ta1, ta2, tb1, tb2)``
     - Return ``True`` when the time interval ``[ta1, ta2]`` overlaps
       the interval ``[tb1, tb2]``. (This can be used with inventories' ``start`` and
       ``end`` fields, in comparison with a user-defined time interval.)


Examples
--------

Applying SEASTERS macros with simple SQL syntax, please find below a series of query
examples to access various information inside the SEASTERS database.

.. literalinclude:: ../../examples/ghcnd.py
   :language: sql
   :caption: Extracted from ``examples/ghcnd.py``
   :lines: 15-22

.. literalinclude:: ../../examples/ghcnh.py
   :language: sql
   :caption: Extracted from ``examples/ghcnh.py``
   :lines: 15-22

.. literalinclude:: ../../examples/gsdr.py
   :language: sql
   :caption: Extracted from ``examples/gsdr.py``
   :lines: 15-23

.. literalinclude:: ../../examples/bsrn.py
   :language: sql
   :caption: Extracted from ``examples/bsrn.py``
   :lines: 15-21
