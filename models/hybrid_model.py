import numpy as np

from tensorflow.keras.models import Model
from tensorflow.keras.layers import (

    Input,
    LSTM,
    Dense,
    Dropout,
    MultiHeadAttention,
    LayerNormalization,
    GlobalAveragePooling1D
)

from tensorflow.keras.optimizers import Adam


def build_hybrid_model(sequence_length, num_features):

    inputs = Input(
        shape=(sequence_length, num_features)
    )

    # -----------------------------
    # LSTM Layer
    # -----------------------------

    x = LSTM(
        64,
        return_sequences=True
    )(inputs)

    x = Dropout(0.2)(x)

    # -----------------------------
    # Transformer Attention Block
    # -----------------------------

    attention_output = MultiHeadAttention(

        num_heads=4,

        key_dim=32

    )(x, x)

    x = LayerNormalization()(x + attention_output)

    # -----------------------------
    # Global Pooling
    # -----------------------------

    x = GlobalAveragePooling1D()(x)

    # -----------------------------
    # Dense Layers
    # -----------------------------

    x = Dense(
        128,
        activation="relu"
    )(x)

    x = Dropout(0.3)(x)

    x = Dense(
        64,
        activation="relu"
    )(x)

    outputs = Dense(
        num_features,
        activation="linear"
    )(x)

    model = Model(
        inputs=inputs,
        outputs=outputs
    )

    model.compile(

        optimizer=Adam(
            learning_rate=0.001
        ),

        loss="mse",

        metrics=["mae"]
    )

    return model


def main():

    # Load training data

    X_train = np.load("X_train.npy")

    y_train = np.load("y_train.npy")

    sequence_length = X_train.shape[1]

    num_features = X_train.shape[2]

    print("\nBuilding Hybrid AI Model...\n")

    model = build_hybrid_model(

        sequence_length,

        num_features
    )

    model.summary()

    print("\nStarting Training...\n")

    history = model.fit(

        X_train,

        y_train,

        epochs=20,

        batch_size=32,

        validation_split=0.2
    )

    # Save model

    model.save("hybrid_missile_ai_model.keras")

    print("\nModel Trained Successfully.\n")

    print("Model Saved Successfully.\n")


if __name__ == "__main__":

    main()