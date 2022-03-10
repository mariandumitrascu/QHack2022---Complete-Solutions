#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def qfunc_adder(m, wires):
    """Quantum function capable of adding m units to a basic state given as input.

    Args:
        - m (int): units to add.
        - wires (list(int)): list of wires in which the function will be executed on.
    """
    binary_m=[int(np.binary_repr(m,width=len(wires))[i]) for i in range(len(wires))]
    qml.QFT(wires=wires)

    # QHACK #
    binary_m=[int(np.binary_repr(m,width=len(wires))[i]) for i in range(len(wires))]
    n=len(wires)
    for p in range(n):
        for k in range(p,n):            
            qml.U1((np.pi/(2**(k-p)))*binary_m[k],wires=wires[n-p-1])
    # QHACK #

    qml.QFT(wires=wires).inv()


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    m = int(inputs[0])
    n_wires = int(inputs[1])
    wires = range(n_wires)

    dev = qml.device("default.qubit", wires=wires, shots=1)

    @qml.qnode(dev)
    def test_circuit():
        # Input:  |2^{N-1}>
        qml.PauliX(wires=0)

        qfunc_adder(m, wires)
        return qml.sample()

    output = test_circuit()
    print(*output, sep=",")
