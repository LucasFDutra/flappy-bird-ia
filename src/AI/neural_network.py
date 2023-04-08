from typing import List
import numpy as np

def tanh(x):
    if x>100: return 1
    elif x < -100: return -1
    return (np.exp(x) - np.exp(-x))/(np.exp(x) + np.exp(-x))

def linear(x):
    return x

def get_function(name):
    if name == 'tanh': return tanh
    if name == 'linear': return linear


class Neuron:
    def __init__(self, activate_function, bias, n_inputs) -> None:
        self.activate_function = activate_function
        self.bias = bias
        self.weights = np.random.randn(n_inputs, 1)

    def calc_output(self, inputs: List[float]):
        # ((x1 * w1) + (x2 * w2) + ... + (xn * wn)) - self.bias
        inputs = np.array(inputs).reshape(1, len(inputs))
        return get_function(self.activate_function)(inputs.dot(self.weights)[0][0] - self.bias)
    
    def mutate(self):
        weights_shape = self.weights.shape
        n_weights_to_mutate = int(weights_shape[0] * np.random.random())
        weights_position = np.random.choice(np.arange(0, weights_shape[0]), n_weights_to_mutate)
        for weight_position in weights_position:
            val = self.weights[weight_position, 0] * np.random.random()
            if np.random.randint(0,1) == 0:
                val = -1*val
            self.weights[weight_position, 0] = self.weights[weight_position, 0] + val

    def get_config(self):
        return {
            'activate_function': self.activate_function,
            'bias': self.bias,
            'weights': self.weights
        }

class Layer:
    def __init__(self, n_neurons, activate_function='tanh', bias=0, previus_layer=None) -> None:
        self.activate_function = activate_function
        self.bias = bias
        self.n_neurons = n_neurons
        self.previus_layer = previus_layer
        self.neurons = None

    def create_neurons(self):
        n_inputs = self.n_neurons if self.previus_layer is None else self.previus_layer.n_neurons
        self.neurons = [
            Neuron(
                activate_function=self.activate_function, 
                bias=self.bias,
                n_inputs=n_inputs
            ) for _ in range(self.n_neurons)
        ]

    def calc(self, inputs: List[float]) -> List[float]:
        res = []
        for neuron in self.neurons:
            res.append(neuron.calc_output(inputs))
        return res

    def mutate(self):
        for neuron in self.neurons:
            neuron.mutate()

    def get_config(self):
        return {
            'activate_function': self.activate_function,
            'bias': self.bias,
            'n_neurons': self.n_neurons,
            'neurons': [neuron.get_config() for neuron in self.neurons]
        }

class NeuralNetwork:
    def __init__(self, config=None) -> None:
        self.layers : List[Layer] = []
        if config:
            self.create_by_config()
    
    def add(self, layer: Layer):
        layer.previus_layer = None if len(self.layers) == 0 else self.layers[-1]
        layer.create_neurons()
        self.layers.append(layer)

    def run(self, inputs: List[float]):
        for i, layer in enumerate(self.layers):
            inputs = layer.calc(inputs)
        return inputs

    def mutate(self):
        for layer in self.layers:
            layer.mutate()

    def get_config(self):
        return [layer.get_config() for layer in self.layers]

    def __repr__(self) -> str:
        text = ''
        for layer in self.layers:
            text += f'n_neurons: {layer.n_neurons} - previus_layer: {layer.previus_layer}\n'
        return text


class BirdAI:
    def __init__(self, bird, nn_params=None) -> None:
        self.bird = bird
        self.nn = self.create_nn(nn_params)

    def create_nn(self, nn_params):
        if not nn_params:
            nn = NeuralNetwork()
            nn.add(Layer(n_neurons=3, activate_function='linear'))
            nn.add(Layer(n_neurons=2, activate_function='linear'))
            nn.add(Layer(n_neurons=1, activate_function='tanh'))
            return nn
        else:
            return NeuralNetwork(nn_params)
    
    def mutate(self):
        self.nn.mutate()

    def play(self, bottom_tube_high, top_tube_high):
        bird_high = self.bird.rect.y + self.bird.size.y * 2
        res = self.nn.run(inputs=[bird_high, bottom_tube_high, top_tube_high])
        if res[0] > 0.5:
            self.bird.go_up()
        else:
            self.bird.go_down()
