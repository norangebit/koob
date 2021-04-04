"""
This module includes the logic needed to interpret the sub-command for annotations.
"""

from typing import List, Dict, OrderedDict, Optional
from koob.kobo import KoboDb, search_kobo_mountpoint
from koob.types import Highlight


def get_highlights(book_title: Optional[str], db: Optional[str], last: bool) -> List[Highlight]:
    """
    Returns the required highlights according to the given parameters.

    :param book_title: title o part of title
    :param db: path of the Kobo database
    :param last: if it is true you only select the highlights of the last highlighted book
    :return: list of highlight
    """

    db_path = db if db is not None \
        else f'{search_kobo_mountpoint()}/.kobo/KoboReader.sqlite'
    db = KoboDb(db_path)

    if len(book_title) != 0:
        return db.get_highlights_by_book_title(' '.join(book_title))
    elif last:
        return db.get_last_highlights()
    else:
        return db.get_all_highlights()


def group_by_chapter(highlights: List[Highlight]) -> Dict[str, Highlight]:
    """
    Group highlights by chapters.

    :param highlights:
    :return: dictionary chapter -> quote
    """
    chapters = list(OrderedDict.fromkeys(hl.chapter for hl in highlights))
    return {ch: [hl for hl in highlights if hl.chapter == ch] for ch in chapters}


def group_by_book(highlights: List[Highlight]) -> Dict[str, Dict[str, List[Highlight]]]:
    """
    Group highlights by books.

    :param highlights: list of highlight
    :return: dictionary book -> chapter -> quote
    """
    books = set([hl.book_title for hl in highlights])
    return {book: group_by_chapter([hl for hl in highlights if hl.book_title == book]) for book in books}
