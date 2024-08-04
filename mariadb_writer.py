import logging
from os import environ
import mariadb
from sqlalchemy import create_engine, MetaData, Table, Column, String , Integer, DateTime
from datetime import datetime

db_config = {
    'PASS': environ.get('PASS', ''),
    'DOMAIN': environ.get('DOMAIN', ''),
    'HASH_SIZE': int(environ.get('HASH_SIZE', '')),
    'RECORDS': int(environ.get('RECORDS', '')),
}
metadata = MetaData()

hashes = Table('hashes', metadata,
               Column('id', Integer, primary_key=True),
               Column('hash', String(640000), unique=True),
               Column('created_at', DateTime, default=datetime.now)
               )


def generate_random_hash(numb: int = 1) -> str:
    import random
    import string
    import hashlib
    if numb == 1:
        return hashlib.sha256(''.join(random.choices(string.ascii_letters + string.digits, k=64)).encode()).hexdigest()
    else:
        return ''.join(
            [hashlib.sha256(''.join(random.choices(string.ascii_letters + string.digits, k=64)).encode()).hexdigest()
             for _ in range(numb)])


def test_mariadb_connection():
    try:
        conn = mariadb.connect(
            user='admin',
            password=db_config['PASS'],
            host=db_config['DOMAIN'],
            port='3306',
            database='db',
        )
        logging.info("MariaDB connection successful")
        conn.close()
        return True
    except Exception as e:
        logging.error(f"MariaDB connection failed: {e}")
        return False


def mariadb_write_hash(size: int = 100) -> bool:
    if test_mariadb_connection():
        maria_uri = f"mysql+pymysql://admin:{db_config['PASS']}@{db_config['DOMAIN']}:3306/db"
        engine = create_engine(maria_uri)
        connection = engine.connect()
        metadata.create_all(engine)
        for _ in range(size):
            connection.execute(hashes.insert().values(hash=generate_random_hash(db_config['HASH_SIZE'])))
        connection.close()
        return True
    return False

if __name__ == '__main__':
    mariadb_write_hash(db_config['RECORDS'])