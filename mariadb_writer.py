import logging
from os import environ
import mariadb
from datetime import datetime

logging.basicConfig(level=logging.INFO)

db_config = {
    'PASS': environ.get('PASS', ''),
    'DOMAIN': environ.get('DOMAIN', ''),
    'HASH_SIZE': int(environ.get('HASH_SIZE', '')),
    'RECORDS': int(environ.get('RECORDS', '')),
}



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
            database='db'
        )
        logging.info("MariaDB connection successful")
        cur = conn.cursor()
        cur.execute("CREATE TABLE hashes (id INT AUTO_INCREMENT PRIMARY KEY, hash TEXT, created_at DATETIME)")
        conn.close()
        return True
    except Exception as e:
        logging.error(f"MariaDB connection failed: {e}")
        return False


def mariadb_write_hash(size: int = 100) -> bool:
    if test_mariadb_connection():
        conn = mariadb.connect(
            user='admin',
            password=db_config['PASS'],
            host=db_config['DOMAIN'],
            database='db',
        )
        cur = conn.cursor()
        for _ in range(size):
            cur.execute(f"INSERT INTO hashes (hash, created_at) VALUES ('{generate_random_hash(db_config['HASH_SIZE'])}', '{datetime.now()}')")
        conn.commit()
        conn.close()

        return True
    return False


if __name__ == '__main__':
    if mariadb_write_hash(db_config['RECORDS']):
        logging.info("Hashes successfully written to the database.")
    else:
        logging.error("Failed to write hashes to the database.")
