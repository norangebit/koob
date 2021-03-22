"""
This module includes the logic needed to interpret the sub-command for books.
"""

from typing import List, Optional

from koob.kobo import KoboDb, search_kobo_mountpoint
from koob.types import Book


def get_books(db: Optional[str], n: int) -> List[Book]:
    """
    Returns the required books according to the given parameters.

    :param db: path of the Kobo database
    :param n: limit to the last n books
    :return: list of book
    """

    db_path = db if db is not None \
        else f'{search_kobo_mountpoint()}/.kobo/KoboReader.sqlite'
    db = KoboDb(db_path)

    return db.get_books(n)
