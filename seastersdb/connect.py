import logging
from typing import Any, Dict

import duckdb
from duckdb.typing import (  # from duckdb.sqltypes import TIMESTAMP, BOOLEAN
    BOOLEAN,
    TIMESTAMP,
)

from ._get_pathdb import get_pathdb

__all__ = ["connect"]

log = logging.getLogger(__name__)


def connect(**read_parquet_kws: Dict[str, Any]) -> duckdb.DuckDBPyConnection:
    """
    Establish a DuckDB connection and register macros and utility functions for
    accessing the SEASTERS database.

    The connection is configured so that all ``read_parquet`` calls use
    ``union_by_name=True`` by default, ensuring consistent schema handling across
    heterogeneous files. The function creates a set of SQL macros that provide
    convenient access to data and metadata for each supported network, as well as
    a dedicated macro for BSRN datasets. A custom ``overlaps`` function is also
    registered for time-range filtering within SQL queries.

    The created macros include:
        - ``ghcnd()``, ``ghcnh()``, ``gsdr()``, ``bsrn()`` for bulk data access.
        - ``<network>_stations()`` and ``<network>_inv()`` for metadata.
        - ``<network>_var()`` for variable definitions (when available).
    A dedicated ``bsrn(dataset)`` macro provides dataset-wise access to BSRN files.
    A custom ``overlaps`` function is added for evaluating temporal coverage in
    SQL queries.

    Parameters
    ----------
    **read_parquet_kws
        Additional keyword arguments forwarded to DuckDB's ``read_parquet``.
        These are applied to all automatically created macros. The option
        ``union_by_name=True`` is always enforced and cannot be overridden.

    Returns
    -------
    con : duckdb.DuckDBPyConnection
        A live DuckDB connection with all SEASTERS macros and custom functions
        registered.
    """
    # Process kwargs
    forced_kws: Dict[str, Any] = dict(union_by_name=True)
    read_parquet_kws.update(forced_kws)

    # Original DuckDB connection
    con = duckdb.connect()
    log.info("Completed connection to DuckDB's API.")

    # Create path macros
    def create_path_macro(name: str, path: str, **kws) -> None:
        str_kws = ", ".join(f"{k} = {v!r}" for k, v in kws.items())
        con.execute(
            f"""
                CREATE MACRO {name}()
                AS TABLE
                FROM read_parquet(
                    '{path}'{(',' + str_kws) if str_kws else ''}
                )
            """  # noqa: E202
        )

    pathdb = get_pathdb()
    for network in ["BSRN", "GHCNd", "GHCNh", "GSDR"]:
        networkl = network.lower()
        if network != "BSRN":
            create_path_macro(
                networkl, f"{pathdb}/{network}/*.parquet", **read_parquet_kws
            )
        create_path_macro(
            f"{networkl}_stations",
            f"{pathdb}/metadata/stations-{networkl}.parquet",
        )
        create_path_macro(
            f"{networkl}_inv",
            f"{pathdb}/metadata/inventory-{networkl}.parquet",
        )
        if network != "GSDR":
            create_path_macro(
                f"{networkl}_var",
                f"{pathdb}/metadata/variables-{networkl}.parquet",
            )
    str_kws = ", ".join(f"{k} = {v!r}" for k, v in read_parquet_kws.items())
    con.execute(
        f"""
        CREATE MACRO bsrn(dataset)
        AS TABLE
        FROM read_parquet(
            '{pathdb}/BSRN/station_id=*/*_' ||
            dataset ||
            '.parquet'
            {(',' + str_kws) if str_kws else ''}
        )
    """  # noqa: E202, E222
    )
    log.info("Created macros to access the SEASTERS database.")

    # Record functions
    def where_overlaps(ta1, ta2, tb1, tb2):
        return tb1 <= ta2 and tb2 >= ta1

    con.create_function("overlaps", where_overlaps, 4 * [TIMESTAMP], BOOLEAN)
    log.info("Created custom functions ('overlaps').")

    return con
