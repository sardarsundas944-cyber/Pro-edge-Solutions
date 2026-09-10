import pickle
import config

def load_model():
    with open(config.MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model

def main():
    print("Loading model from:", config.MODEL_PATH)
    model = load_model()

    sample = [[5.1, 3.5, 1.4, 0.2]]
    result = model.predict(sample)
    print("Prediction for sample flower:", result[0])

if __name__ == "__main__":
    main()
