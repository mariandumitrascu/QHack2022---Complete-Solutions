#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


dev = qml.device("default.qubit", wires=[0, 1,"sol"], shots=1)


def find_the_car(oracle):
    """Function which, given an oracle, returns which door that the car is behind.

    Args:
        - oracle (function): function that will act as an oracle. The first two qubits (0,1)
        will refer to the door and the third ("sol") to the answer.

    Returns:
        - (int): 0, 1, 2, or 3. The door that the car is behind.
    """
        
    def Ufo():
        for i in range(2):
            qml.Hadamard(wires=i)
        qml.PauliZ(wires=0)
        qml.PauliZ(wires=1)
        qml.CZ(wires=[0,1])
        for i in range(2):
            qml.Hadamard(wires=i)

    @qml.qnode(dev)
    def circuit1():
        # QHACK #
        qml.BasisState(np.array([0,0,0]),wires=[0,1,"sol"])
        for i in range(2):
            qml.Hadamard(wires=i)
        qml.PauliX(wires="sol")
        qml.Hadamard(wires="sol")
        oracle()
        Ufo()
        # QHACK #
        return qml.sample()

    @qml.qnode(dev)
    def circuit2(params):
        # QHACK #
        qml.BasisState(np.array([params[0],params[1],0]),wires=[0,1,"sol"])
        oracle()
        # QHACK #
        return qml.sample()

    sol1 = circuit1()
    sol2 = circuit2(sol1)

    # QHACK #

    # process sol1 and sol2 to determine which door the car is behind.
    
    return 1*sol1[1]+2*sol1[0]

    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    numbers = [int(i) for i in inputs]

    def oracle():
        if numbers[0] == 1:
            qml.PauliX(wires=0)
        if numbers[1] == 1:
            qml.PauliX(wires=1)
        qml.Toffoli(wires=[0, 1, "sol"])
        if numbers[0] == 1:
            qml.PauliX(wires=0)
        if numbers[1] == 1:
            qml.PauliX(wires=1)

    output = find_the_car(oracle)
    print(f"{output}")
