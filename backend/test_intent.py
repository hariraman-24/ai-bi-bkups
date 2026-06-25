from intent_classifier import IntentClassifier

classifier = IntentClassifier()

print(classifier.classify("Show sales"))
print(classifier.classify("Give revenue report"))
print(classifier.classify("Read csv file"))
print(classifier.classify("Who is the president"))