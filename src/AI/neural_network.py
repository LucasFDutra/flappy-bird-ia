from typing import List
import numpy as np
import json

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
    def __init__(self, activate_function, bias, n_inputs, weights, max_variation) -> None:
        self.activate_function = activate_function
        self.bias = bias
        self.weights = np.random.randn(n_inputs, 1) if weights is None else weights
        self.max_variation = max_variation

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
            if val > self.max_variation: val = self.max_variation
            if val < -self.max_variation: val = -self.max_variation
            if np.random.randint(0,1) == 0:
                val = -1*val
            self.weights[weight_position, 0] = self.weights[weight_position, 0] + val

class Layer:
    def __init__(self, n_neurons, activate_function='tanh', bias=0, previus_layer=None, max_variation=0.2) -> None:
        self.activate_function = activate_function
        self.bias = bias
        self.n_neurons = n_neurons
        self.previus_layer = previus_layer
        self.neurons = None
        self.max_variation = max_variation

    def create_neurons(self, weights):
        n_inputs = self.n_neurons if self.previus_layer is None else self.previus_layer.n_neurons
        if weights is None:
            weights = [None for _ in range(self.n_neurons)]

        self.neurons = [
            Neuron(
                activate_function=self.activate_function, 
                bias=self.bias,
                n_inputs=n_inputs,
                weights=w,
                max_variation=self.max_variation
            ) for w in weights
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
            'max_variation': self.max_variation,
            'neurons': [neuron.weights.tolist() for neuron in self.neurons]
        }

class NeuralNetwork:
    def __init__(self, config=None) -> None:
        self.layers : List[Layer] = []
        if config:
            self.create_by_config(config)
    
    def add(self, layer: Layer, weights=None):
        layer.previus_layer = None if len(self.layers) == 0 else self.layers[-1]
        layer.create_neurons(weights)
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
    
    def save(self, file_path):
        with open(file_path, 'w') as f:
            json.dump(self.get_config(), f, indent=4)

    def create_by_config(self, config):
        for layer in config:
            self.add(Layer(
                n_neurons=layer.get('n_neurons'),
                activate_function=layer.get('activate_function'),
                bias=layer.get('bias'),
                max_variation=layer.get('max_variation')
            ), weights=[np.array(w) for w in layer.get('neurons')])

    def load(self, file_path):
        with open(file_path, 'r') as f:
            self.create_by_config(json.load(f))

    def __repr__(self) -> str:
        text = ''
        for layer in self.layers:
            text += f'n_neurons: {layer.n_neurons} - previus_layer: {layer.previus_layer}\n'
        return text


class BirdAI:
    def __init__(self, bird, nn_config=None, max_variation=0.2) -> None:
        self.bird = bird
        self.bird.ai_points = 0
        self.max_variation = max_variation
        self.nn = self.create_nn(nn_config)

    def create_nn(self, config):
        if not config:
            nn = NeuralNetwork()
            nn.add(Layer(n_neurons=3, activate_function='linear', max_variation=self.max_variation))
            nn.add(Layer(n_neurons=2, activate_function='linear', max_variation=self.max_variation))
            nn.add(Layer(n_neurons=1, activate_function='tanh', max_variation=self.max_variation))
            return nn
        else:
            return NeuralNetwork(config)
    
    def mutate(self):
        self.nn.mutate()

    def play(self, bottom_tube_high, top_tube_high):
        bird_high = self.bird.rect.y + self.bird.size.y * 2
        d_bottom = abs(bird_high - bottom_tube_high)
        d_top = abs(bird_high - top_tube_high)
        self.bird.ai_points = self.bird.points - (d_bottom + d_top)
        res = self.nn.run(inputs=[bird_high, bottom_tube_high, top_tube_high])
        if res[0] > 0.5:
            self.bird.go_up()
        else:
            self.bird.go_down()

    def get_config(self):
        return self.nn.get_config()
    
    def save(self, file_path):
        self.nn.save(file_path)
