#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np


dev = qml.device("default.qubit", wires=2)


def prepare_entangled(alpha, beta):
    """Construct a circuit that prepares the (not necessarily maximally) entangled state in terms of alpha and beta
    Do not forget to normalize.

    Args:
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>
    """

    # QHACK #
    theta=2*np.arccos(alpha/np.sqrt(alpha**2+beta**2))
    qml.RY(theta,wires=0)
    qml.CNOT(wires=[0,1])
    # QHACK #

@qml.qnode(dev)
def chsh_circuit(theta_A0, theta_A1, theta_B0, theta_B1, x, y, alpha, beta):
    """Construct a circuit that implements Alice's and Bob's measurements in the rotated bases

    Args:
        - theta_A0 (float): angle that Alice chooses when she receives x=0
        - theta_A1 (float): angle that Alice chooses when she receives x=1
        - theta_B0 (float): angle that Bob chooses when he receives x=0
        - theta_B1 (float): angle that Bob chooses when he receives x=1
        - x (int): bit received by Alice
        - y (int): bit received by Bob
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (np.tensor): Probabilities of each basis state
    """

    prepare_entangled(alpha, beta)

    # QHACK #
    theta_alice=theta_A0*(1-x)+x*theta_A1
    theta_bob=theta_B0*(1-y)+y*theta_B1
    
    qml.adjoint(qml.RY)(2*theta_alice,wires=0)
    qml.adjoint(qml.RY)(2*theta_bob,wires=1)
    # QHACK #

    return qml.probs(wires=[0, 1])
    

def winning_prob(params, alpha, beta):
    """Define a function that returns the probability of Alice and Bob winning the game.

    Args:
        - params (list(float)): List containing [theta_A0,theta_A1,theta_B0,theta_B1]
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (float): Probability of winning the game
    """

    # QHACK #
    s=0.0
    
    for x in range(2):
        for y in range(2):
            probs=chsh_circuit(params[0], params[1], params[2], params[3], x, y, alpha, beta)
            if (x*y==0):
                s+=(probs[0]+probs[3])*0.25
            if (x*y==1):
                s+=(probs[1]+probs[2])*0.25
        
    return s
    # QHACK #
    

def optimize(alpha, beta):
    """Define a function that optimizes theta_A0, theta_A1, theta_B0, theta_B1 to maximize the probability of winning the game

    Args:
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (float): Probability of winning
    """

    def cost(params):
        return ((1-winning_prob(params, alpha, beta))**2)
        """Define a cost function that only depends on params, given alpha and beta fixed"""

    # QHACK #

    #Initialize parameters, choose an optimization method and number of steps
    np.random.seed(42)
    init_params = np.array([0.1,0.1,0.1,0.1], requires_grad=True)
    opt = qml.AdamOptimizer(stepsize=0.4)
    steps = 300

    # QHACK #
    
    # set the initial parameter values
    params = init_params

    for i in range(steps):
        # update the circuit parameters 
        # QHACK #
        params = opt.step(cost, params)
        # QHACK #

    return winning_prob(params, alpha, beta)


if __name__ == '__main__':
    inputs = sys.stdin.read().split(",")
    output = optimize(float(inputs[0]), float(inputs[1]))
    print(f"{output}")