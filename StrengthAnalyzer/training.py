from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pickle

# Reading the data-set
output = pd.read_csv("/home/santhoshtk/Music/Advanced-Password-Manager-CLI/StrengthAnalyzer/data.csv",
                     sep=",",
                     on_bad_lines='skip')

# Separate the training and testing set
X = output['password']
y = output['strength']

# Convert the passwords into vectors.
tfidf_vectorizer = TfidfVectorizer(max_features=1)
X = tfidf_vectorizer.fit_transform(X.values.astype('U'))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Creating the instance of the model and training.
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Saving the model as a pickle file for further predictions.
with open("/home/santhoshtk/Music/Advanced-Password-Manager-CLI/StrengthAnalyzer/RFCModel.pkl", mode='wb') as modelFile:
    pickle.dump(model, modelFile)
