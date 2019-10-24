from app.db import books, shop_books
from sqlalchemy.sql import select, and_
import logging

class Shop:
    @classmethod
    async def list_books(cls, shop_id: int, conn):
        cur = await conn.execute(
            select([shop_books, books], use_labels=True).
            select_from(shop_books.join(books))
            .where(shop_books.c.shop_id == shop_id)
        )
        rows = await cur.fetchall()
        return rows

    @classmethod
    def book_to_dict(cls, book):
        return {
            'book_id': book['books_id'],
            'title': book['books_title'],
            'author': book['books_author'],
        }

