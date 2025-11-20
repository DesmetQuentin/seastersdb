import logging
from importlib.resources import as_file, files
from pathlib import Path

__all__ = ["get_pathdb"]

log = logging.getLogger(__name__)


def get_pathdb() -> Path:
    """Return the path to the database's root directory.

    The root directory is defined in ``seastersdb/data/path.txt``. The file must
    exist and contain a valid absolute path pointing to the database location.

    Returns
    -------
    pathdb : Path
        The resolved root directory of the database.

    Raises
    ------
    FileNotFoundError
        If ``path.txt`` is missing or if the path stored inside the file does
        not exist.
    """
    try:
        resource = files("seastersdb.data").joinpath("path.txt")
        with resource.open("r") as file:
            pathdb = Path(file.read())
    except FileNotFoundError:
        with as_file(resource) as real_path:
            pathtxt = str(real_path)
        log.error("'%s' not found.", pathtxt)
        log.error("This file should exist and contain the database's root directory.")
        raise FileNotFoundError("'%s' not found.", pathtxt)

    if not pathdb.exists():
        with as_file(resource) as real_path:
            pathtxt = str(real_path)
        raise FileNotFoundError("Path in '%s' ('%s') does not exist.", pathtxt, pathdb)

    return pathdb
