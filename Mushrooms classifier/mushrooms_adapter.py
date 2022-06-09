# importing libraries


import csv
import psycopg2
import numpy as np


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
        self.connection = psycopg2.connect(dbname="mushrooms", user="postgres", password="****") # not my actual password
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "DROP TABLE IF EXISTS mushrooms")
        self.cursor.execute("""
            CREATE TABLE mushrooms 
            (
            class int,
            cap-shape int,
            cap-surface int,
            cap-color int,
            bruises int,
            odor int,
            gill-attachment int,
            gill-spacing int,
            gill-size int,
            gill-color int,
            stalk-shape int,
            stalk-root int,
            stalk-surface-above-ring int,
            stalk-surface-below-ring int,
            stalk-color-above-ring int,
            stalk-color-below-ring int,
            veil-type int,
            veil-color int,
            ring-number int,
            ring-type int,
            spore-print-color int,
            population int,
            habitat int
            );
            """.replace("-", "_"))
        self.connection.commit()

    def write_data(self, file="mushrooms.csv"):
        """
        Function, that writes converted data (chars into integers, because ml algorithm takes numbers) to the database
        :param file: file with data to write
        :return: self
        """
        with open(file, newline="") as f:
            data = list(csv.reader(f, delimiter=','))
            for _ in data[1::]:
                _ = list(map(lambda __: ord(__), _))
                self.cursor.execute("""
                    INSERT INTO mushrooms
                    VALUES 
                    (
                    %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, 
                    %s, %s, %s
                    );
                    """, _)
        self.connection.commit()
        return self

    def get_target(self):
        """
        Function, that returns targets from database
        (first column in db, targets == classes to classify, in this project it's edible or poisonous)
        :return: numpy array of data
        """
        self.cursor.execute(
            "SELECT class FROM mushrooms")
        data = self.cursor.fetchall()
        self.connection.commit()
        return np.array(data).reshape(len(data), )

    def get_data(self):
        """
        Function, that returns data from database
        (all columns in db except first, in this project it's mushroom's characteristics)
        :return: numpy array of data
        """
        self.cursor.execute("""
            SELECT 
            cap-shape,
            cap-surface,
            cap-color,
            bruises,
            odor,
            gill-attachment,
            gill-spacing,
            gill-size,
            gill-color,
            stalk-shape,
            stalk-root,
            stalk-surface-above-ring,
            stalk-surface-below-ring,
            stalk-color-above-ring,
            stalk-color-below-ring,
            veil-type,
            veil-color,
            ring-number,
            ring-type,
            spore-print-color,
            population,
            habitat
            FROM mushrooms
            """.replace("-", "_"))
        data = self.cursor.fetchall()
        self.connection.commit()
        return np.array(data)

    def __str__(self):
        return f"Adapter"

    def __del__(self):
        """
        closing connections
        """
        self.cursor.close()
        self.connection.close()