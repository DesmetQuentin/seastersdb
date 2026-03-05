import io
import sys
from typing import Callable

from duckdb import DuckDBPyConnection

from ..connect import connect
from .viewer import Viewer


def main() -> None:

    def query_wrapper(con: DuckDBPyConnection) -> Callable[[str], str]:
        def function(query: str) -> str:
            buffer = io.StringIO()
            sys.stdout = buffer
            con.sql(query).show(max_width=1000)
            sys.stdout = sys.__stdout__
            return buffer.getvalue()

        return function

    def export_wrapper(con: DuckDBPyConnection) -> Callable[[str, str], None]:
        def function(filename: str, query: str) -> None:
            df = con.sql(query).df()
            df.to_csv(filename, index=False)

        return function

    con = connect()
    viewer = Viewer(query_wrapper(con), export_wrapper(con), title="SEASTERSdb")
    viewer.run()


if __name__ == "__main__":
    main()
