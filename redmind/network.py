from redmind.layers import Layer, Dense
import numpy as np
import redmind.functions as fn
import matplotlib.pyplot as plt
from typing import List
from redmind.dataloader import Dataloader

class NeuralNetwork:
    def __init__(self, layers: List[Layer], verbose=False, cost_function = fn.mse, grad_function = fn.mse_prime) -> None:
        self.layers = layers
        self.costs = {}
        self._verbose = verbose
        self.cost_function = cost_function
        self.grad_function = grad_function
        if self._verbose:
            print(f"Neural Network initialized with {len(self.layers)} layers")

    def details(self) -> None:
        for index, layer in enumerate(self.layers):
            print(f"Layer {index + 1} {layer}")

    def forward(self, x: np.ndarray = None) -> np.ndarray:
        out = x
        for layer in self.layers:
            out = layer.forward(x = out)
        return out

    def backward(self, gradient: float = None, learning_rate: float = None) -> None:
        grad = gradient
        for layer in reversed(self.layers):
            grad = layer.backward(output_gradient=grad, learning_rate=learning_rate)
        return None

    def predict(self, x: np.ndarray = None):
        return self.forward(x)

    def set_train(self, state=False):
        if self._verbose:
            print(f"updating NN layers training to: {state}")
        for layer in self.layers:
            layer.set_train(state=state)

    def set_verbose(self, state):
        assert type(state) == bool
        self._verbose = state

    def train(self, X: np.ndarray = None, Y: np.ndarray = None, epochs: int =20, n_batches: int = 1, learning_rate: float = 0.1, early_stoping: float = 0.0):
        data = Dataloader(X=X, Y=Y, n_batches=n_batches)
        #print(data)
        self.set_train(state=True)
        if self._verbose:
            if n_batches > 1:
                print(f"Starting train with {n_batches} batches of size {data} ")
        for epoch in range(epochs):
            for x, y in data:
                # forward
                y_pred = self.forward(x=x)
                # calculate error and cost
                cost = self.cost_function(y, y_pred)
                self.costs[epoch] = cost
                error_gradient = self.grad_function(y, y_pred)
                # backward
                self.backward(gradient=error_gradient, learning_rate=learning_rate)
            # print cost to console
            accuracy = round(100 - (self.costs[epoch] * 100), 3)
            if self._verbose:
                print(f"epoch: {epoch + 1}/{epochs}, cost: {round(self.costs[epoch], 4)}, accuracy: {accuracy}%")
            if early_stoping > 0.0:
                if accuracy >= early_stoping:
                    print("Training stoped learning due to early stoping")
                    break
        self.set_train(state=False)

    def graph_costs(self) -> None:
        plt.plot(list(self.costs.keys()), list(self.costs.values()))
        plt.xlabel("Epoch")
        plt.ylabel("Cost")
        plt.show()