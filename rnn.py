import lyrics_generation.helper as hlp
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Activation, Flatten, Dropout, Dense, Embedding, TimeDistributed, CuDNNLSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

# Hyperparameters
SEQ_LENGTH = 100
LAYERS_NUM = 2
LAYER_SIZE = [256, 256, 256]


def main():
    dataset = hlp.get_dataset()
    dataset = dataset[:10000]
    chars = sorted(list(set(dataset)))
    dataset_size = len(dataset)
    vocab_size = len(chars)
    idx_to_char = {i: ch for i, ch in enumerate(chars)}
    char_to_idx = {ch: i for i, ch in enumerate(chars)}

    # Make training examples
    print("Making training examples...")
    X = list()
    Y = list()

    for i in range(0, dataset_size - SEQ_LENGTH):
        input_seq = dataset[i:i+SEQ_LENGTH]
        label_seq = dataset[i+SEQ_LENGTH]
        X.append([char_to_idx[ch] for ch in input_seq])
        Y.append(char_to_idx[label_seq])

    n_examples = len(X)

    print(f"Finished with making training examples with total number {n_examples}")

    # Reshape examples
    X = np.reshape(X, (n_examples, SEQ_LENGTH, 1))
    # Normalize input data
    X = X / float(vocab_size)
    # One-hot encode output data
    Y = np_utils.to_categorical(Y)

    # Make the model
    print("Start making the model")
    model = Sequential()

    model.add(LSTM(LAYER_SIZE[0], input_shape=(X.shape[1], X.shape[2]), return_sequences=True))  # input layer

    for i in range(1, LAYERS_NUM):
        model.add(LSTM(LAYER_SIZE[i], return_sequences=True))  # hidden layers

    model.add(Flatten())  # flatten last hidden layer

    model.add(Dense(Y.shape[1]))
    model.add(Activation("softmax"))
    model.compile(loss="categorical_crossentropy", optimizer="adam")

    model.summary()

    print("Finished with making the model")

    # Configure checkpoint through callbacks
    checkpoint_name = "Weights-LSTM-improvement-{epoch:03d}-{loss:.5f}.hdf5"
    checkpoint = ModelCheckpoint(checkpoint_name, monitor="loss", verbose=1, save_best_only=True, mode="min")
    callbacks_list = [checkpoint]

    # Do the training
    model_params = {"epochs": 30,
                    "batch_size": 128,
                    "callbacks": callbacks_list,
                    "verbose": 1,
                    "validation_split": 0.2,
                    "validation_data": None,
                    "shuffle": True,
                    "initial_epoch": 0,
                    "steps_per_epoch": None,
                    "validation_steps": None}

    model.fit(X,
              Y,
              epochs=model_params["epochs"],
              batch_size=model_params["batch_size"],
              callbacks=model_params["callbacks"],
              verbose=model_params["verbose"],
              validation_split=model_params["validation_split"],
              validation_data=model_params["validation_data"],
              shuffle=model_params["shuffle"],
              initial_epoch=model_params["initial_epoch"],
              steps_per_epoch=model_params["steps_per_epoch"],
              validation_steps=model_params["validation_steps"])


def generate_lyrics():
    # Load the weights
    weights_file = "./Weights-LSTM-improvement-003-3.09039.hdf5"

    # Generate lyrics


if __name__ == '__main__':
    main()
    # generate_lyrics()
