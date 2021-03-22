from typing import List
import re


class Book:
    def __init__(
            self,
            id: str,
            title: str,
            authors: str,
            publisher: str,
            percent_reading: int,
            eta: int,
            reading_time: int
    ):
        self.id: str = id
        self.title: str = title
        self.authors: List[str] = authors.replace(' and ', ', ')\
            .split(', ')
        self.publisher = publisher
        self.percent_reading = percent_reading
        self.eta = eta
        self.reading_time = reading_time

    def __str__(self):
        return f'id = {self.id}, title = {self.title}, authors = {self.authors}, publisher = {self.publisher}'

    def is_completed(self) -> bool:
        return self.percent_reading == 100

    def is_started(self) -> bool:
        return self.percent_reading != 0

    def get_reading_status(self) -> str:
        if self.is_completed():
            return ''
        elif self.is_started():
            return f'{self.percent_reading}%'
        else:
            return ''


class Highlight:
    def __init__(self, id: str, book_title: str, chapter: str, text: str):
        self.id: str = id
        self.book_title: str = book_title
        self.chapter: str = chapter
        self.text: str = re.sub(r'\s+', ' ', text)\
            .strip()

    def __str__(self):
        return f'id = {self.id}, book = {self.book_title}, chapter = {self.chapter}, text = {self.text}'
