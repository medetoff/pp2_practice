import psycopg2
from config import load_config


def connect():
    config = load_config()
    conn = psycopg2.connect(**config)
    conn.autocommit = True
    return conn


if __name__ == '__main__':
    conn = connect()
    print('Connected.')
    conn.close()