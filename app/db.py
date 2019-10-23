from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime,
    create_engine, MetaData,
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

sessions = Table(
    'sessions', meta,
    Column('id', Integer, primary_key=True),
    Column('session_key', String(36), nullable=False, unique=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('created_dt', DateTime, server_default=text('now()')),
)

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"

def create_tables(engine):
    meta = MetaData(bind=engine)
    tables=[users, sessions]
    meta.drop_all(tables=tables)
    meta.create_all(bind=engine, tables=tables)

def sample_data(engine):
    conn = engine.connect()
    conn.execute(users.insert(), [
        {'login': 'user1', 'password': hash_password('test@pass'), 'email': 'test@example.com'},
    ])
    conn.close()

def init_db():
    db_url = DSN.format(**config['pg'])
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)

