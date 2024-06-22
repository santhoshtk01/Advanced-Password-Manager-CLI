import pickle
from training import convert_password_to_vector


def predict(password: str) -> int:
    # 0 - low, 1 - moderate, 2 - high
    vector = convert_password_to_vector(password)

    # Load the model
    with open("/home/santhoshtk/Music/Advanced-Password-Manager-CLI/StrengthAnalyzer/RFCModel.pkl", "rb") as model_file:
        model = pickle.load(model_file)

    output = model.predict([vector])
    return output
