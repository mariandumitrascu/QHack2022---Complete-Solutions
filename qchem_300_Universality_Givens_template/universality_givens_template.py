#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np


def givens_rotations(a, b, c, d):
    """Calculates the angles needed for a Givens rotation to out put the state with amplitudes a,b,c and d

    Args:
        - a,b,c,d (float): real numbers which represent the amplitude of the relevant basis states (see problem statement). Assume they are normalized.

    Returns:
        - (list(float)): a list of real numbers ranging in the intervals provided in the challenge statement, which represent the angles in the Givens rotations,
        in order, that must be applied.
    """

    # QHACK #
    dev = qml.device('default.qubit', wires=6)

    @qml.qnode(dev)
    def circuit(params):
        qml.BasisState(np.array([1, 1, 0, 0, 0, 0]), wires=[0, 1, 2, 3, 4, 5])
        qml.DoubleExcitation(params[0], wires=[0, 1, 2, 3])
        qml.DoubleExcitation(params[1], wires=[2, 3, 4, 5])
        # single excitations controlled on qubit 0
        qml.ctrl(qml.SingleExcitation, control=0)(params[2], wires=[1, 3])
        return qml.state()

    def cost_fn(params):
        res=circuit(params)
        return np.abs((res[48]-a)**2+(res[12]-b)**2+(res[3]-c)**2+(res[36]-d)**2)

    
    opt = qml.GradientDescentOptimizer(stepsize=0.4)
    epochs = 1000
    angles = np.array([0.005,0.005,0.005], requires_grad=True)

    for epoch in range(epochs):
        angles,cost = opt.step_and_cost(cost_fn, angles)

    return angles
    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    theta_1, theta_2, theta_3 = givens_rotations(
        float(inputs[0]), float(inputs[1]), float(inputs[2]), float(inputs[3])
    )
    print(*[theta_1, theta_2, theta_3], sep=",")
