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


class RnnModel:

    def __init__(self):
        print("Initializing dataset and vocabulary...")

        self.dataset = hlp.get_dataset()[:100000]
        self.dataset_size = len(self.dataset)
        self.vocab = sorted(list(set(self.dataset)))
        self.vocab_size = len(self.vocab)
        self.idx_to_char = {i: ch for i, ch in enumerate(self.vocab)}
        self.char_to_idx = {ch: i for i, ch in enumerate(self.vocab)}
        self.examples = list()
        self.labels = list()
        self.num_of_examples = 0
        self.model = None

        print("Finished with initialization!")

    def make_examples(self):
        # Make training examples
        print("Making training examples...")
        self.examples = list()
        self.labels = list()

        for i in range(0, self.dataset_size - SEQ_LENGTH):
            example_seq = self.dataset[i:i + SEQ_LENGTH]
            label_seq = self.dataset[i + SEQ_LENGTH]
            self.examples.append([self.char_to_idx[ch] for ch in example_seq])
            self.labels.append(self.char_to_idx[label_seq])

        self.num_of_examples = len(self.examples)

        print(f"Finished with making training examples with total number {self.num_of_examples}")

    def make_model(self):
        x, y = self.prepare_examples()

        # Make the model
        print("Start making the model")
        self.model = Sequential()

        self.model.add(LSTM(LAYER_SIZE[0], input_shape=(x.shape[1], x.shape[2]), return_sequences=True))  # input layer

        for i in range(1, LAYERS_NUM):
            self.model.add(LSTM(LAYER_SIZE[i], return_sequences=True))  # hidden layers

        self.model.add(Flatten())  # flatten last hidden layer

        self.model.add(Dense(y.shape[1]))
        self.model.add(Activation("softmax"))
        self.model.compile(loss="categorical_crossentropy", optimizer="adam")

        self.model.summary()

        print("Finished with making the model")

    def train(self):
        # Configure checkpoint through callbacks
        checkpoint_name = "Weights-LSTM-improvement-{epoch:03d}-{loss:.5f}.hdf5"
        checkpoint = ModelCheckpoint(checkpoint_name, monitor="loss", verbose=1, save_best_only=True, mode="min")
        callbacks_list = [checkpoint]

        x, y = self.prepare_examples()

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

        self.model.fit(x,
                       y,
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

    def generate_lyrics(self):
        # Load the weights
        weights_file = "./models/model_01/Weights-LSTM-improvement-030-0.00771.hdf5"
        self.model.load_weights(weights_file)
        self.model.compile(loss="categorical_crossentropy", optimizer="adam")

        # Generate lyrics
        start = np.random.randint(0, self.num_of_examples-1)
        pattern = self.examples[start]
        print("Seed:")
        print(self.reverse_to_chars(pattern))

        num_of_chars = 300
        output = list()

        for i in range(num_of_chars):
            x = np.reshape(pattern, (1, len(pattern), 1))
            x = x / float(self.vocab_size)
            prediction = self.model.predict(x, verbose=0)
            idx = np.argmax(prediction)
            res = self.idx_to_char[idx]
            output.append(res)
            pattern.append(res)
            pattern = pattern[1:len(pattern)]

        print("Output:")
        print("".join(output))
        print("-----")
        print("Finished with generation!")

    def prepare_examples(self):
        # Reshape examples
        x = np.reshape(self.examples, (self.num_of_examples, SEQ_LENGTH, 1))
        # Normalize input data
        x = x / float(self.vocab_size)
        # One-hot encode output data
        y = np_utils.to_categorical(self.labels)

        return x, y

    def reverse_to_chars(self, l):
        if type(l) is int:
            return self.idx_to_char[l]

        temp = list()
        for idx in l:
            temp.append(self.idx_to_char[idx])

        return "".join(temp)


if __name__ == '__main__':

    model = RnnModel()
    model.make_examples()
    model.make_model()
    model.generate_lyrics()
