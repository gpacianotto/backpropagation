import numpy as np

class Perceptron:
    def __init__(self, num_inputs):
        # Initialize weights and bias
        self.weights = np.random.rand(num_inputs)
        self.bias = np.random.rand()
    
    def activate(self, x):
        # Activation function (step function)
        return 1 if x >= 0 else 0
    
    def forward(self, inputs):
        # Weighted sum (dot product) plus bias
        weighted_sum = np.dot(self.weights, inputs) + self.bias
        # Apply activation function
        return self.activate(weighted_sum)
    
    def update_weights(self, inputs, error, learning_rate):
        # Update weights based on the error and learning rate
        self.weights += learning_rate * error * inputs
        self.bias += learning_rate * error

class NeuralNetwork:
    def __init__(self, num_inputs, num_neurons):
        # Initialize network with specified number of neurons
        self.neurons = [Perceptron(num_inputs) for _ in range(num_neurons)]
    
    def forward(self, inputs):
        # Get outputs for each neuron in the network
        return [neuron.forward(inputs) for neuron in self.neurons]
    
    def train(self, training_data, labels, epochs, learning_rate):
        for epoch in range(epochs):
            for inputs, label in zip(training_data, labels):
                # Forward pass through each neuron
                outputs = self.forward(inputs)
                for i, neuron in enumerate(self.neurons):
                    # Calculate error for each neuron
                    error = label[i] - outputs[i]
                    # Update weights and bias based on the error
                    neuron.update_weights(np.array(inputs), error, learning_rate)
