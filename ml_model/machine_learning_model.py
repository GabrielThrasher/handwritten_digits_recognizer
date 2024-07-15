import datetime
import pickle

from ml_model import mnist_loader as mnist_loader
from program_info.program_wide_imports import *


class Network:
    def __init__(self, sizes, trained_weights=None, trained_biases=None,
                 dev_testing=False, testing_data=None):
        # NN properties
        self.num_layers = len(sizes)
        self.num_mid_layers = self.num_layers - 1
        self.sizes = sizes

        # Initializing weights to either ones that were already trained, if
        # given, otherwise ones from a random distribution
        if trained_weights:
            self.weights = trained_weights
        else:
            self.weights = [np.random.randn(y, x)
                            for x, y in zip(sizes[:-1], sizes[1:])]

        # Initializing biases to either ones that were already trained, if
        # given, otherwise ones from a random distribution
        if trained_biases:
            self.biases = trained_biases
        else:
            self.biases = [np.random.randn(x) for x in sizes[1:]]

        # For dev time and status keeping
        if dev_testing:
            self.dev_testing = dev_testing
            self.start_times = {}
            self.testing_data = testing_data

    def train(self, data, epoch_num, data_points_per_batch, eta):
        # Train the NN model to get the best weights and biases for the given
        # data set
        self.eta = eta
        self.num_data_pts = len(data)

        num_batches = round(self.num_data_pts / data_points_per_batch)

        if self.dev_testing:
            self.start_time(
                dev_type="train",
                message="\nStarting training..."
            )

        for i in range(epoch_num):
            if self.dev_testing:
                self.start_time(
                    dev_type="epoch",
                    message=f"Beginning epoch {i + 1}..."
                )

            # Randomly shuffle data then partition into batches and split inputs
            # from outputs
            np.random.shuffle(data)
            data_input_batches = self.partition_into_batches(
                [data_input[0] for data_input in data], num_batches
            )
            data_output_batches = self.partition_into_batches(
                [data_output[1] for data_output in data], num_batches
            )

            # Perform batch updates for NN model
            for j in range(len(data_input_batches)):
                self.batch_update(data_input_batches[j], data_output_batches[j])

            if self.dev_testing:
                self.end_time(
                    dev_type="epoch",
                    message=f"epoch {i + 1} completed | Current model "
                    f"accuracy: {self.evaluate(self.testing_data)}%",
                    milisecs=True
                )

        if self.dev_testing:
            self.end_time(
                dev_type="train",
                message=f"training session completed\n",
                milisecs=True
            )

    def partition_into_batches(self, data_list, num_batches):
        # Partitions a list into num_batches approximately equal parts for the
        # batches
        length = len(data_list)
        part_size = length // num_batches
        remainder = length % num_batches

        parts = []
        start = 0
        for i in range(num_batches):
            end = start + part_size + (1 if i < remainder else 0)
            parts.append(data_list[start:end])
            start = end

        return parts

    def batch_update(self, data_inputs, data_outputs):
        # Used for backpropagation
        self.weight_derivatives = []
        self.bias_derivatives = []
        data_pts_in_batch = len(data_inputs)

        # For each data pt in a batch
        for i in range(data_pts_in_batch):
            self.feedforward(data_inputs[i])
            self.backpropagate(data_outputs[i], i)

        # Update the weights and biases based on the derivatives calculated
        for i in range(self.num_mid_layers):
            self.weights[i] -= (self.weight_derivatives[i] /
                                data_pts_in_batch) * self.eta
            self.biases[i] -= (self.bias_derivatives[i].flatten() /
                               data_pts_in_batch) * self.eta

    def feedforward(self, data_inputs):
        # Feed the inputs through each NN layer to calculate the a values
        # throughout, including the final layer which is the output
        self.a_values = [data_inputs]

        for i in range(self.num_mid_layers):
            self.calc_layer_a_values(
                self.a_values[i],
                self.weights[i],
                self.biases[i]
            )

    def calc_layer_a_values(self, outputs, weights, biases):
        # Calculate the a values for a particular NN layer
        dot_products = np.array([])
        num_next_layer = len(biases)

        for i in range(num_next_layer):
            weights_partial = weights[i]
            dot_products = np.append(
                dot_products, np.dot(weights_partial.T, outputs)
            )

        self.a_values.append(self.activation_function(dot_products + biases))

    def activation_function(self, z):
        # Neuron activation function
        return 1 / (1 + np.exp(-z))

    def backpropagate(self, data_outputs, data_point_num):
        # Backpropagate through the NN layers to calculate the weight and bias
        # derivatives
        # For each mid_layer
        for x in range(self.num_mid_layers - 1, -1, -1):
            a1 = self.a_values[x].reshape(len(self.a_values[x]), )
            a2 = self.a_values[x + 1].reshape(len(self.a_values[x + 1]), 1)

            # If the last mid-layer
            if x == self.num_mid_layers - 1:
                self.v_values = 2 * a2 * (1 - a2) * (
                        a2 - data_outputs.reshape((len(data_outputs), 1)))
            else:
                dot = np.dot(self.weights[x + 1].T, self.v_values)
                self.v_values = a2 * (1 - a2) * dot

            weight_der = a1 * self.v_values

            # If the first data point in the batch
            if data_point_num == 0:
                self.weight_derivatives.insert(0, weight_der)
                self.bias_derivatives.insert(0, self.v_values)
            else:
                self.weight_derivatives[x] += weight_der
                self.bias_derivatives[x] += self.v_values

    def evaluate(self, testing_data):
        # Evaluate the accuracy of the NN model out of 100%
        num_accurate = 0
        data_inputs = [data_input[0] for data_input in testing_data]
        data_outputs = [data_input[1] for data_input in testing_data]

        for i in range(len(data_inputs)):
            prediction = np.argmax(self.predict(data_inputs[i]))
            if prediction == data_outputs[i]:
                num_accurate += 1

        return 100 * num_accurate / len(testing_data)

    def predict(self, data_input):
        # Predict the value from the trained NN model given an input
        self.feedforward(data_input)

        return self.a_values[-1]

    def start_time(self, dev_type, message=None):
        # Dev function for keeping track of time and status of NN training
        self.start_times[dev_type] = datetime.datetime.now()
        if message:
            print(message)

    def end_time(self, dev_type, message, milisecs=False):
        # Dev function for keeping track of time and status of NN training
        self.end = datetime.datetime.now()
        time_diff = str(self.end - self.start_times[dev_type])

        if milisecs:
            end_idx = len(time_diff) + 1
        else:
            end_idx = time_diff.find(".")
        time_diff = time_diff[time_diff.find(":") + 1:end_idx]

        print(f"Time elapsed: {time_diff} | {message}")


def get_best_model(best_of, highest_accuracy, training_data, validation_data):
    # Determines the most accurate model from a set a hyperparameters and saves
    # its weights, biases, and sizes for future use
    highest_accuracy_idx = 0
    saved_model = False
    accuracies = []

    for i in range(best_of):
        print("\n-------------------------------------------------------------")
        print(f"Training session {i + 1}:")
        net = Network(
            sizes=[784, 100, 10],
            dev_testing=True,
            testing_data=validation_data
        )
        net.train(
            data=training_data,
            epoch_num=20,
            data_points_per_batch=10,
            eta=0.3
        )

        accuracy = net.evaluate(validation_data)
        accuracies.append(accuracy)
        if accuracy > highest_accuracy:
            highest_accuracy = accuracy
            highest_accuracy_idx = i
            saved_model = True

            pickle.dump(
                highest_accuracy,
                open("ml_model/saved_ml_model/highest_accuracy.pkl", "wb")
            )
            pickle.dump(
                net.sizes,
                open("ml_model/saved_ml_model/sizes.pkl", "wb")
            )
            pickle.dump(
                net.weights,
                open("ml_model/saved_ml_model/weights.pkl", "wb")
            )
            pickle.dump(
                net.biases,
                open("ml_model/saved_ml_model/biases.pkl", "wb")
            )

        print(
            f"Training session: {i + 1} | Current accuracy: {accuracy}% | "
            f"Highest accuracy: {highest_accuracy}%"
        )
        print("-------------------------------------------------------------")

    print("*************************************************************")
    print("Training Session Grouping Status Report")
    print("*************************************************************")
    for i in range(len(accuracies)):
        print(f"Training Session {i}: {accuracies[i]}%")

    if saved_model:
        print(
            f"Saved NN model with an accuracy of {highest_accuracy}% "
            f"(training session: {highest_accuracy_idx + 1})"
        )
    else:
        print(
            f"Did not save any NN models from this grouping as all were "
            f"below the current highest accuracy of {highest_accuracy}%"
        )
    print("*************************************************************")


def predict_number(data_input):
    sizes = pickle.load(open("ml_model/saved_ml_model/sizes.pkl", "rb"))
    weights = pickle.load(open("ml_model/saved_ml_model/weights.pkl", "rb"))
    biases = pickle.load(open("ml_model/saved_ml_model/biases.pkl", "rb"))
    net = Network(sizes, trained_weights=weights, trained_biases=biases)

    return net.predict(data_input)


def get_NN_model_accuracy():
    return pickle.load(
        open("ml_model/saved_ml_model/highest_accuracy.pkl", "rb")
    )


def main():
    # Load in digit data
    training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
    training_data, validation_data, test_data = \
        list(training_data), list(validation_data), list(test_data)

    train = True
    if train:
        # Training NN model numerous times to get the most accurate
        highest_accuracy = pickle.load(
            open("saved_ml_model/highest_accuracy.pkl", "rb")
        )
        get_best_model(
            best_of=3,
            highest_accuracy=highest_accuracy,
            training_data=training_data,
            validation_data=validation_data
        )

    # Loading in saved, most accurate NN model
    sizes = pickle.load(open("saved_ml_model/sizes.pkl", "rb"))
    weights = pickle.load(open("saved_ml_model/weights.pkl", "rb"))
    biases = pickle.load(open("saved_ml_model/biases.pkl", "rb"))
    net = Network(sizes, trained_weights=weights, trained_biases=biases)

    print(
        f"\nEvaluating NN model on test data yields an accuracy of "
        f"{net.evaluate(test_data)}%"
    )


if __name__ == "__main__":
    main()
