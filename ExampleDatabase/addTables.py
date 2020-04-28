import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def delete_table(conn, delete_table_sql):
    try:
        c = conn.cursor()
        c.execute(delete_table_sql)
    except Error as e:
        print(e)

def main():
    database = r"test.db"

    products_table = """ CREATE TABLE IF NOT EXISTS products (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        shelflife integer 
                                    );"""
    
    months_table = """ CREATE TABLE IF NOT EXISTS months (
                                    id integer PRIMARY KEY,
                                    month text NOT NULL
                                );"""

    stock_table = """CREATE TABLE IF NOT EXISTS stock (
                                    product_id integer PRIMARY KEY,
                                    qty integer,
                                    packageSize integer,
                                    addedDate date NOT NULL,
                                    manufactured date NOT NULL,
                                    FOREIGN KEY (product_id) REFERENCES products (id)
                                );"""

    product_history_table = """ CREATE TABLE IF NOT EXISTS history (
                                        history_id integer PRIMARY KEY,
                                        product_id integer NOT NULL,
                                        added_date date NOT NULL,
                                        removed_date date NOT NULL,
                                        actualRate integer NOT NULL,
                                        FOREIGN KEY (product_id) REFERENCES products (id)
                                    );"""

    estimation_per_month_table = """ CREATE TABLE IF NOT EXISTS estimatedRates (
                                        month_id integer,
                                        product_id integer,
                                        estimatedRate integer,
                                        FOREIGN KEY (month_id) REFERENCES months (id),
                                        FOREIGN KEY (product_id) REFERENCES products (id),
                                        PRIMARY KEY(product_id, month_id)
                                    );"""
    
    drop_estimations_table = """DROP TABLE estimatedRates;"""
    drop_history_table = """DROP TABLE history;"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create tables
        #create_table(conn, products_table)
        #create_table(conn, stock_table)
        #create_table(conn, product_history_table)
        #create_table(conn, months_table)
        #create_table(conn, estimation_per_month_table)

        #delete_table(conn, drop_estimations_table)
        #create_table(conn, estimation_per_month_table)

        delete_table(conn, drop_history_table)
        create_table(conn, product_history_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()