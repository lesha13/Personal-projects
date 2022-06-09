# importing libraries


import psycopg2


class Adapter:
    """
    Class, to work with database (PostgreSQL)
    using psycopg2
    """

    def __init__(self):
        """
        initialization,
        opening connections,
        dropping and creating new table (for my convenience)
        """
        self.connection = psycopg2.connect(dbname="stocks", user="postgres", password="****") # not my actual password
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "DROP TABLE IF EXISTS stocks")
        self.cursor.execute(
            "CREATE TABLE stocks (ticker text PRIMARY KEY, price real, url text)")
        self.connection.commit()

    def write_data(self, ticker: str, price: float, url: str):
        """
        Function, that writes data  to the database
        :param ticker: ticker of the company
        :param price: price of the stock
        :param url: url on https://finance.yahoo.com
        :return: None
        """
        self.cursor.execute("INSERT INTO stocks VALUES (%s, %s, %s);", (ticker, price, url))
        self.connection.commit()

    def get_data(self):
        """
        Function, that returns data from database
        :return: data
        """
        self.cursor.execute("SELECT price, ticker FROM stocks")
        data = self.cursor.fetchall()
        self.connection.commit()
        return data

    def __str__(self):
        return f"Adapter"

    def __del__(self):
        """
        closing connections
        """
        self.cursor.close()
        self.connection.close()
