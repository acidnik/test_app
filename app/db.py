from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime,
    create_engine, MetaData, UniqueConstraint
)
from sqlalchemy.sql.expression import text
from app.settings import config
from app.user.utils import hash_password

meta = MetaData()

users = Table(
    'users', meta,

    Column('id', Integer, primary_key=True),
    Column('login', String(200), nullable=False, unique=True),
    Column('password', String(40), nullable=False),
    Column('email', String(200), nullable=False),
    Column('created_dt', DateTime, server_default=text('now()')),
)

books = Table(
    'books', meta,
    Column('id', Integer, primary_key=True),
    Column('title', String(512), nullable=False),
    Column('author', String(512), nullable=False),
    UniqueConstraint('title', 'author'),
)

shops = Table(
    'shops', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(512), nullable=False, unique=True),
)

orders = Table(
    'orders', meta,
    Column('id', Integer, primary_key=True),
    Column('amount', Integer, nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False, index=True),
    Column('shop_id', Integer, ForeignKey('shops.id'), nullable=False, index=True),
    Column('book_id', Integer, ForeignKey('books.id'), nullable=False, index=True),
    UniqueConstraint('user_id', 'book_id', 'shop_id'),
)

def create_tables(engine):
    meta = MetaData(bind=engine)
    tables=[users, books, shops, orders]
    meta.drop_all(tables=tables)
    meta.create_all(bind=engine, tables=tables)

def sample_data(engine):
    conn = engine.connect()
    conn.execute(users.insert(), [
        {'login': 'user1', 'password': hash_password('test@pass'), 'email': 'test@example.com'},
        {'login': 'user2', 'password': hash_password('test@pass2'), 'email': 'test2@example.com'},
    ])
    conn.execute(books.insert(), [
        # {'title': '', 'author': ''},
        {'title': 'Москва-Петушки', 'author': 'Венедикт Ерофеев'},
        {'title': 'Война и мир', 'author': 'Лев Толстой'},
        {'title': 'Евгений Онегин', 'author': 'Александр Пушкин'},
    ])
    conn.execute(shops.insert(), [
        {'name': 'Boson'},
    ])
    conn.execute(orders.insert(), [
        {'amount': 1, 'user_id': 1, 'shop_id': 1, 'book_id': 1},
        {'amount': 1, 'user_id': 1, 'shop_id': 1, 'book_id': 2},
    ])
    conn.close()

def init_db():
    DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"

    db_url = DSN.format(**config['pg'])
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)

