import sys
import pennylane as qml
from pennylane import numpy as np
import pennylane.optimize as optimize
from pennylane.optimize import AdamOptimizer
from pennylane.optimize import NesterovMomentumOptimizer
DATA_SIZE = 250


def square_loss(labels, predictions):
    """Computes the standard square loss between model predictions and true labels.

    Args:
        - labels (list(int)): True labels (1/-1 for the ordered/disordered phases)
        - predictions (list(int)): Model predictions (1/-1 for the ordered/disordered phases)

    Returns:
        - loss (float): the square loss
    """

    loss = 0
    for l, p in zip(labels, predictions):
        loss = loss + (l - p) ** 2

    loss = loss / len(labels)
    return loss


def accuracy(labels, predictions):
    """Computes the accuracy of the model's predictions against the true labels.

    Args:
        - labels (list(int)): True labels (1/-1 for the ordered/disordered phases)
        - predictions (list(int)): Model predictions (1/-1 for the ordered/disordered phases)

    Returns:
        - acc (float): The accuracy.
    """

    acc = 0
    for l, p in zip(labels, predictions):
        if abs(l - p) < 1e-5:
            acc = acc + 1
    acc = acc / len(labels)

    return acc


def classify_ising_data(X, Y):
    """Learn the phases of the classical Ising model.

    Args:
        - ising_configs (np.ndarray): 250 rows of binary (0 and 1) Ising model configurations
        - labels (np.ndarray): 250 rows of labels (1 or -1)

    Returns:
        - predictions (list(int)): Your final model predictions

    Feel free to add any other functions than `cost` and `circuit` within the "# QHACK #" markers 
    that you might need.
    """

    # QHACK #
    
    def layer(W):

        qml.RX(W[0, 0], wires=0)
        qml.RX(W[1, 0], wires=1)
        qml.RX(W[2, 0], wires=2)
        qml.RX(W[3, 0], wires=3)
        
        qml.RZ(W[0, 1], wires=0)
        qml.RZ(W[1, 1], wires=1)
        qml.RZ(W[2, 1], wires=2)
        qml.RZ(W[3, 1], wires=3)

        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[2, 3])
        qml.CNOT(wires=[3, 0])
    
    
    def statepreparation(x):
        qml.BasisState(x, wires=[0, 1, 2, 3])

    num_wires = ising_configs.shape[1] 
    dev = qml.device("default.qubit", wires=num_wires) 

    # Define a variational circuit below with your needed arguments and return something meaningful
    @qml.qnode(dev)
    def circuit_no_bias(weights,x):
        
        statepreparation(x)

        for W in weights:
            layer(W)
            
        return qml.expval(qml.PauliZ(0))
    
    def circuit(weights,bias,x):
        return circuit_no_bias(weights,x)+bias

    # Define a cost function below with your needed arguments
    def cost(weights,bias,X,Y):

        # QHACK #
        
        # Insert an expression for your model predictions here
        predictions = [circuit(weights,bias,x) for x in X]

        # QHACK #

        return square_loss(Y, predictions) # DO NOT MODIFY this line

    # optimize your circuit here
    np.random.seed(0)
    
    num_layers = 3
    weights_init = 0.01 * np.random.randn(num_layers, num_wires, 2, requires_grad=True)
    bias_init = np.array(0.0, requires_grad=True)
   
   
    
    opt = AdamOptimizer(0.5)
    epochs = 25
   
    
    weights=weights_init
    bias=bias_init
   
    for epoch in range(epochs):
        #print(epoch)
        #print(weights.shape)
        #batches
        #batch_index = np.random.randint(0, len(X), (batch_size,))
        #X_batch = X[batch_index]
        #Y_batch = Y[batch_index]
        #weights,bias,_,_,cost_fun=opt.step_and_cost(cost, weights,bias, X, Y)
        weights,bias,_,_=opt.step(cost, weights,bias, X, Y)
     
    
        
        #print(weights)
        predictions=[int(np.sign(circuit(weights,bias,x))) for x in X]        
        acc=accuracy(Y,predictions)
        
        #print(f"Iter: {epoch}  | Accuracy: {acc} ")
        if(acc>0.9):
            break
        
    
    return predictions
    


if __name__ == "__main__":
    inputs = np.array(
        sys.stdin.read().split(","), dtype=int, requires_grad=False
    ).reshape(DATA_SIZE, -1)
    ising_configs = inputs[:, :-1]
    labels = inputs[:, -1]
    predictions = classify_ising_data(ising_configs, labels)
    print(*predictions, sep=",")
