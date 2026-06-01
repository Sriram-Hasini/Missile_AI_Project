import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split


SEQUENCE_LENGTH = 20


def load_dataset(file_path):

    df = pd.read_csv(file_path)

    print("\nDataset Loaded Successfully.\n")

    print(df.head())

    return df


def preprocess_data(df):

    # Remove timestamp and phase columns
    feature_columns = [

        col for col in df.columns

        if col not in [
            "timestamp",
            "operational_phase",
            "mission_status"
        ]
    ]

    data = df[feature_columns]

    scaler = MinMaxScaler()

    scaled_data = scaler.fit_transform(data)

    print("\nData Normalized Successfully.\n")

    return scaled_data, scaler, feature_columns


def create_sequences(data, sequence_length):

    X = []
    y = []

    for i in range(len(data) - sequence_length):

        X.append(
            data[i:i + sequence_length]
        )

        y.append(
            data[i + sequence_length]
        )

    X = np.array(X)
    y = np.array(y)

    return X, y


def split_dataset(X, y):

    X_train, X_test, y_train, y_test = train_test_split(

        X,
        y,

        test_size=0.2,

        random_state=42,

        shuffle=False
    )

    return X_train, X_test, y_train, y_test


def main():

    file_path = "missile_telemetry_data.csv"

    df = load_dataset(file_path)

    scaled_data, scaler, feature_columns = preprocess_data(df)

    X, y = create_sequences(
        scaled_data,
        SEQUENCE_LENGTH
    )

    print("\nSequence Generation Completed.\n")

    print(f"Input Shape: {X.shape}")

    print(f"Target Shape: {y.shape}")

    X_train, X_test, y_train, y_test = split_dataset(X, y)

    print("\nTrain-Test Split Completed.\n")

    print(f"Training Samples: {len(X_train)}")

    print(f"Testing Samples: {len(X_test)}")

    np.save("X_train.npy", X_train)
    np.save("X_test.npy", X_test)

    np.save("y_train.npy", y_train)
    np.save("y_test.npy", y_test)

    print("\nPreprocessed datasets saved successfully.\n")


if __name__ == "__main__":

    main()