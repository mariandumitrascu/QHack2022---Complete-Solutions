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

    # QHACK 
    dev = qml.device("default.qubit", wires=8,shots=1)
    @qml.qnode(dev)
    def oracle():
        
        # output qubit 2
        qml.PauliX(wires=2)
        qml.Hadamard(wires=2)

        for i in range(2):
            qml.Hadamard(wires=i)
        # first two entries two th oracle [0,1]
        #output wire 2
        qml.PauliX(wires=5)
        qml.Hadamard(wires=5)
        # [3,4] wires for fi
        for i in range(3,5):
            qml.Hadamard(wires=i)
        #controlled fi with wires [0,1]
        # if 00 apply f0, 01 apply f1, 10 apply f2, 11 apply f3 on [3,4] controlled by [0,1]
        # aditional 2 wires for controll [6 , 7]
        qml.PauliX(wires=0)
        qml.PauliX(wires=1)
        qml.CNOT(wires=[0,6])
        qml.CNOT(wires=[1,7])
        qml.PauliX(wires=0)
        qml.PauliX(wires=1)
        
        qml.ctrl(fs[3], control=[0,1])([3,4,5])
        qml.ctrl(fs[0], control=[6,7])([3,4,5])
        qml.ctrl(fs[1], control=[1,6])([3,4,5])
        qml.ctrl(fs[2], control=[0,7])([3,4,5])
        
        
        for i in range(3,5):
            qml.Hadamard(wires=i)
            
        qml.MultiControlledX(control_wires=[3,4], wires=2, control_values='00')
        
        #kharaf
        for i in range(3,5):
            qml.Hadamard(wires=i)
        qml.adjoint(qml.ctrl(fs[3], control=[0,1]))([3,4,5])
        qml.adjoint(qml.ctrl(fs[0], control=[6,7]))([3,4,5])
        qml.adjoint(qml.ctrl(fs[1], control=[1,6]))([3,4,5])
        qml.adjoint(qml.ctrl(fs[2], control=[0,7]))([3,4,5])
        for i in range(3,5):
            qml.Hadamard(wires=i)
            
        qml.CNOT(wires=[0,6])
        qml.CNOT(wires=[1,7])
        
        for i in range(2):
            qml.Hadamard(wires=i)   

        return qml.probs(wires=[0,1])
    
    
    val=oracle()
    #print(val)
    ch="4 same"
    if (val[0]<0.1):
        ch="2 and 2"
       
    return ch
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
