Python API
==========

.. admonition:: Not comfortable coding in Python?

   Then prefer using the :doc:`interactive session <interactive>`!


The Python API is named ``seastersdb``. In a Python script, you can import it with,
e.g., the following snippet:

.. code:: python

   import seastersdb as sdb


The package actually provides one single function named
:func:`~seastersdb.connect.connect` which returns a `DuckDB connection
<https://duckdb.org/docs/stable/clients/python/reference/#duckdb.DuckDBPyConnection>`_
to the SEASTERS database (calling the function creates the connection and defines the
various macros and functions listed :ref:`here <macros>`).
The API thus simply consists of using the connection and its methods.

Retrieve the connection with the following command:

.. code:: python

   con = sdb.connect()


.. note::

   Since :func:`~seastersdb.connect.connect` is the only function of ``seastersdb``, an
   alternative workflow could be written this way:

   .. code:: python

      from seastersdb import connect

      con = connect()


From here, executing an :ref:`SQL query <sql>` can be done with the `execute()
<https://duckdb.org/docs/stable/clients/python/reference/#duckdb.DuckDBPyConnection.execute>`_
method:

.. code:: python

   # Example query
   query = """
   SELECT *
   FROM ghcnd_stations()
   """

   con.execute(query)


Then, calling the `df()
<https://duckdb.org/docs/stable/clients/python/reference/#duckdb.DuckDBPyConnection.df>`_
method right after executing a query allows actually
extracting the query's result as a `pandas.DataFrame()
<https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame>`_
object:

.. code:: python

   df = con.df()


Afterwards, `pandas <https://pandas.pydata.org/docs/>`_ is quite a popular tool in
our field and there are many resources on the internet to deal with it. Also, a
`pandas.DataFrame()
<https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame>`_
can be converted into objects from other popular Python packages like `xarray
<https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_xarray.html#pandas.DataFrame.to_xarray>`_,
and be exported to files in various formats, such as in `csv
<https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html#pandas.DataFrame.to_csv>`_.
Nevertheless, if your goal is to export your query's result in a file, using the
:doc:`interactive session <interactive>` should be a more adequate solution.
