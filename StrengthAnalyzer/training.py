import string
import pickle
import pandas as pd

from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


# Function to convert a password into vector
def convert_password_to_vector(password: str):
    output_vector = [0, 0, 0, 0, 0]

    # Check if the password length exceeds 8
    if len(password) >= 8:
        output_vector[4] = 1

    for char in password:
        if char in string.ascii_lowercase:
            output_vector[0] = 1
        elif char in string.ascii_uppercase:
            output_vector[1] = 1
        elif char in string.digits:
            output_vector[2] = 1
        elif char in string.punctuation:
            output_vector[3] = 1

    return output_vector


# Reading the data-set
output = pd.read_csv("/home/santhoshtk/Music/Advanced-Password-Manager-CLI/StrengthAnalyzer/data_set.csv",
                     sep=",",
                     on_bad_lines='skip')


# Build the X, y with clean data.
X = []
y = []

# Filter out unwanted data from the dataset.
for password, strength in zip(output['password'], output['strength']):
    X.append(convert_password_to_vector(password))
    y.append(strength)


# Split the data for training and testing.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create an instance of the Random Forest Classifier and train the model.
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model as a serializable object.
with open("/home/santhoshtk/Music/Advanced-Password-Manager-CLI/StrengthAnalyzer/RFCModel.pkl", mode="wb") as model_file:
    pickle.dump(model, model_file)

# Test the model with the test data set. 30% of data from the original.
predictions = model.predict(X_test)
accuracy = accuracy_score(predictions, y_test)
report = classification_report(predictions, y_test)

# Save the test report as a text file.
with open("/home/santhoshtk/Music/Advanced-Password-Manager-CLI/StrengthAnalyzer/reports.txt", mode="w") as report_file:
    report_file.write(f"Test accuracy score : {accuracy}")
    report_file.write(report)
