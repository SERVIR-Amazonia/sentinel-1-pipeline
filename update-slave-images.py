import psycopg2
import csv
from datetime import date, datetime, timedelta


def connect_to_db(db):
    try:
        connection_parameters = 'dbname=%s user=%s host=%s password=%s' % (db['dbname'], db['user'], db['host'], db['password'])
        conn = psycopg2.connect(connection_parameters)
    except Exception as e:
        print 'problem connecting to the database!'
        logging.error(e)
    else:
        return conn, conn.cursor()

def close_connection(cur, conn):
    cur.close()
    conn.close()

db = {
    'dbname': 'DATABASE',
    'user': 'USERNAME',
    'host': 'localhost',
    'password': 'PASSWORD'
}

with open('slaves.csv') as csv_file:
    slaves = csv.reader(csv_file)
    for slave in slaves:
        conn, cur = connect_to_db(db)
        try:
            cur.execute("UPDATE sentinel1 SET slave=TRUE WHERE title='{}'".format(slave[0]))
            conn.commit()
        except Exception as e:
            print('error with updating because {}'.format(e))
            continue
        else:
            close_connection(conn, cur)
