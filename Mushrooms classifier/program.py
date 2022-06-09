# importing files with main code


from mushrooms_adapter import Adapter
from mushrooms_ml_classifier import Classifier

if __name__ == "__main__":
    adapter = Adapter()
    adapter.write_data()
    classifier = Classifier(adapter)

    mushrooms = classifier.data[1][0:5]     # some mushrooms to predict
    print(classifier.predict(mushrooms))
