"""
This module includes all the code necessary for interaction with the user through the command line.
Interaction takes place via the click library.
"""

import click

from typing import List, Optional

from koob.books import get_books
from koob.types import Highlight, Book
from koob.annotations import get_highlights, group_by_book


@click.group()
def koob():
    pass


@koob.command(help='Extracts highlights, bookmarks and notes.')
@click.argument('book_title', nargs=-1, required=False)
@click.option('-l', '--last', type=bool, is_flag=True, help='Selects annotations only from the last annotated book.')
@click.option('--md', type=bool, is_flag=True, help='The output is formatted in markdown.')
@click.option('--db',
              type=click.Path(exists=True),
              help='The path to the Kobo database. If this field is omitted koob searches for the Kobo among the connected devices.'
              )
def annotations(book_title: str, db: Optional[str], last: bool, md: bool):
    """
    Function for the 'annotations' sub-command.
    """
    highlights = get_highlights(book_title, db, last)

    if md:
        display_highlights_markdown(highlights)
    else:
        display_highlights(highlights)

    if len(book_title) != 0 and last:
        click.secho('\nThe last flag is ignored when searching by book title.', fg='yellow')


@koob.command(help='Lists books.')
@click.option('-n', type=int, help='The max number of books to list.', default=-1)
@click.option('--db',
              type=click.Path(exists=True),
              help='The path to the Kobo database. If this field is omitted koob searches for the Kobo among the connected devices.'
              )
def books(db: Optional[str], n: int):
    """
    Function for the 'books' sub-command.
    """
    books = get_books(db, n)

    display_books(books)


def display_highlights(hls: List[Highlight]):
    """
    This function print a list of highlights on the screen.
    """
    for hl in hls:
        click.echo(f'{hl.book_title} - {hl.chapter}')
        click.echo(f'\t{hl.text}')


def display_highlights_markdown(hls: List[Highlight]):
    """
    This function print a list of highlights on the screen.
    Printing is done in a format similar to markdown.
    """
    hls_dict = group_by_book(hls)

    for book in hls_dict:
        click.echo(f'# {book}\n')
        for chapter in hls_dict[book]:
            click.echo(f'- {chapter}')
            for hl in hls_dict[book][chapter]:
                click.echo(f'  - {hl.text}')
        click.echo()


def display_books(books: List[Book]):
    """
    This function print a list of books on the screen.
    """
    for (i, book) in zip(range(1, len(books)), books):
        click.echo(f'{i}. {book.title} by {" & ".join(book.authors)}', nl=False)
        click.echo(f' {book.get_reading_status()}')


if __name__ == '__main__':
    koob()
