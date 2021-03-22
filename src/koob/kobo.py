"""
This module includes code to interact with a kobo e-reader.
"""

import sqlite3
from typing import List, Optional
from blkinfo import BlkDiskInfo
from koob.types import Book, Highlight


class KoboDb:
    """
    This class allows interaction with the kobo sql database.
    """

    def __init__(self, db_path: str):
        self.__connection = sqlite3.connect(db_path)

    def __get_user_id(self) -> str:
        """
        Returns the user ID.
        Assumes that there is only one user.

        :return: user id
        """

        cursor = self.__connection \
            .execute('select UserID from user limit 1')

        return cursor.fetchone()[0]

    def __get_books_id(self, title: str) -> List[str]:
        """
        Returns all books whose title starts with the given string.

        :param title: title or part of title
        :return: list of book is
        """

        user = self.__get_user_id()
        cursor = self.__connection \
            .execute("select ContentID from content where ContentType = 6 and ___UserID = ? and Title like ?",
                     [user, f'{title}%'])

        return [row[0] for row in cursor]

    def __get_book_id_of_last_annotation(self) -> str:
        """
        Returns the identifier of the last book that was annotated.

        :return: book id
        """

        cursor = self.__connection \
            .execute("select VolumeID from Bookmark order by DateCreated desc limit 1")

        return cursor.fetchone()[0]

    def get_books(self, last: int = -1) -> List[Book]:
        """
        Returns the user's list of books.
        The list can be limited to only the last n elements.

        :param last: Indicates the limit of books to be retrieved. -1 indicates no limit
        :return: list of book id
        """

        user = self.__get_user_id()
        cursor = self.__connection \
            .execute("select ContentID, Title, Attribution, Publisher, ___PercentRead, RestOfBookEstimate, "
                     "TimeSpentReading from content "
                     "where ContentType = 6 and ___UserID = ? "
                     "order by DateLastRead desc limit ?",
                     [user, last]
                     )

        return [Book(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in cursor]

    def get_all_highlights(self) -> List[Highlight]:
        """
        Returns all highlights.

        :return: list of highlight
        """

        cursor = self.__connection \
            .execute("select BookmarkId, BookTitle, Title, Text, Bookmark.DateCreated "
                     "from Bookmark left join content content.ContentID like Bookmark.ContentID|| '%' "
                     "where ContentType = 899 and Text != ''"
                     )

        return [Highlight(row[0], row[1], row[2], row[3]) for row in cursor]

    def get_highlights_by_book_title(self, book_title: str) -> List[Highlight]:
        """
        Returns all highlights that belong to books that match the given title.

        :param book_title: title or part of title
        :return: list of highlight
        """

        books_id = self.__get_books_id(book_title)
        results = [self.get_highlights_by_book_id(id) for id in books_id]
        return [h for highlights in results for h in highlights]

    def get_highlights_by_book_id(self, book_id: str) -> List[Highlight]:
        """
        Returns all highlights that belong to the given book.

        :param book_id: id of the book
        :return: list of highlight
        """

        cursor = self.__connection \
            .execute("select BookmarkId, BookTitle, Title, Text, Bookmark.DateCreated "
                     "from Bookmark left join content on content.ContentID like Bookmark.ContentID|| '%' "
                     "where ContentType = 899 and Text != '' and VolumeId = ?",
                     [book_id]
                     )

        return [Highlight(row[0], row[1], row[2], row[3]) for row in cursor]

    def get_last_highlights(self) -> List[Highlight]:
        """
        Returns all highlights belonging to the last highlighted book.

        :return: list of highlight
        """

        return self.get_highlights_by_book_id(
            self.__get_book_id_of_last_annotation()
        )


def search_kobo_mountpoint() -> Optional[str]:
    """
    This function search for the Kobo mountpoint.
    In case the device is not mounted, not connected or there are more than one device it raises an exception.
    This function uses lsblk.
    """
    myblkd = BlkDiskInfo()
    filters = {'label': 'KOBOeReader'}
    kobos = myblkd.get_disks(filters)

    kobo_number = len(kobos)
    if kobo_number == 0:
        raise RuntimeError('No device could be identified.')
    elif kobo_number != 1:
        raise RuntimeError('Several devices have been identified.')
    else:
        mp = kobos[0]['mountpoint']
        if mp == '':
            raise RuntimeError('The device has not been mounted.')
        else:
            return mp


if __name__ == '__main__':
    print(search_kobo_mountpoint())
