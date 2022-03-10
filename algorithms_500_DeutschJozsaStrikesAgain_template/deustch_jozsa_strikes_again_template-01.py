#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def deutsch_jozsa(fs):
    """Function that determines whether four given functions are all of the same type or not.

    Args:
        - fs (list(function)): A list of 4 quantum functions. Each of them will accept a 'wires' parameter.
        The first two wires refer to the input and the third to the output of the function.

    Returns:
        - (str) : "4 same" or "2 and 2"
    """

    # QHACK #

    f1 = fs[0]
    f2 = fs[1]
    f3 = fs[2]
    f4 = fs[3]


    dev = qml.device("default.qubit", wires=5)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.Hadamard(wires=1)
        f1([0, 1, 2])
        f2([0, 1, 3])
        f3([0, 1, 4])
        # f4([0, 1, 5])

        # return  qml.expval(qml.PauliZ(wires=2)), qml.expval(qml.PauliZ(wires=3)), qml.expval(qml.PauliZ(wires=4)), qml.expval(qml.PauliZ(wires=5))
        return  qml.expval(qml.PauliZ(wires=2)), qml.expval(qml.PauliZ(wires=3)), qml.expval(qml.PauliZ(wires=4))

    res = circuit()
    output = '4 same'
    n_balanced = 0
    for i in res:
        if i==0:
            n_balanced += 1
    if n_balanced==2:
        output = '2 and 2'

    return output

    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    numbers = [int(i) for i in inputs]

    # Definition of the four oracles we will work with.

    def f1(wires):
        qml.CNOT(wires=[wires[numbers[0]], wires[2]])
        qml.CNOT(wires=[wires[numbers[1]], wires[2]])

    def f2(wires):
        qml.CNOT(wires=[wires[numbers[2]], wires[2]])
        qml.CNOT(wires=[wires[numbers[3]], wires[2]])

    def f3(wires):
        qml.CNOT(wires=[wires[numbers[4]], wires[2]])
        qml.CNOT(wires=[wires[numbers[5]], wires[2]])
        qml.PauliX(wires=wires[2])

    def f4(wires):
        qml.CNOT(wires=[wires[numbers[6]], wires[2]])
        qml.CNOT(wires=[wires[numbers[7]], wires[2]])
        qml.PauliX(wires=wires[2])

    output = deutsch_jozsa([f1, f2, f3, f4])
    print(f"{output}")
