# importing libraries


# to work with data
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mglearn as mgl

from sklearn.ensemble import GradientBoostingClassifier     # didn't use
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split


class Classifier:

    def __init__(self, adapter):
        """
        initialization,
        using adapter from mushrooms_adapter.py file,
        getting data using methods,
        choosing model
        (I chose Support Vector Machine due to multi-dimensionality idk if it's a good choice i'm just training)
        :param adapter: adapter to work with database
        """
        self.adapter = adapter
        self.data = self.prepare_data()
        self.model = self.svc_model()

    def prepare_data(self):
        """
        Function, that returns divided data (target/data train/test) for ml algorithm
        using methods from adapter
        :return: x_train, x_test, y_train, y_test (x == data, y == target)
        """
        data = self.adapter.get_data()
        target = self.adapter.get_target()
        x_train, x_test, y_train, y_test = train_test_split(data, target, random_state=13)
        return x_train, x_test, y_train, y_test

    def knc_model(self):
        """
        Function, that creates ml alg obj
        (KNeighborsClassifier),
        trains model using our prepared data,
        prints score of predicting on the data
        :return: KNeighborsClassifier obj
        """
        knc = KNeighborsClassifier(n_neighbors=3)
        knc.fit(self.data[0], self.data[2])
        print(f"Train score: {knc.score(self.data[0], self.data[2])}")
        print(f"Test  score: {knc.score(self.data[1], self.data[3])}")
        return knc

    def svc_model(self):
        """
        Function, that creates ml alg obj
        (SVC),
        trains model using our prepared data
        :return: SVC obj
        """
        svc = SVC()
        svc.fit(self.data[0], self.data[2])
        print(f"Train score: {svc.score(self.data[0], self.data[2])}")
        print(f"Test  score: {svc.score(self.data[1], self.data[3])}")
        return svc

    """
    We can also add a lot more ml algs if we want
    """

    def predict(self, data):
        """
        Function, that returns predicts targets with given data
        :param data:
        :return: list of predictions
        """
        return [chr(_.item()) for _ in self.model.predict(data.reshape(-1, 22))]

    def plot(self):
        """
        Function, that makes plot
        (Not ready)
        :return: None
        """
        pass

    def __str__(self):
        return f"Classifier"

    def __del__(self):
        pass
