#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def switch(oracle):
    """Function that, given an oracle, returns a list of switches that work by executing a
    single circuit with a single shot. The code you write for this challenge should be completely
    contained within this function between the # QHACK # comment markers.

    Args:
        - oracle (function): oracle that simulates the behavior of the lights.

    Returns:
        - (list(int)): List with the switches that work. Example: [0,2].
    """

    dev = qml.device("default.qubit", wires=[0, 1, 2, "light"], shots=1)
    
    def Ufo():
        for i in range(3):
            qml.Hadamard(wires=i)
        #qml.Hadamard(wires="light")
        arr=np.eye(2**4)
        for i in range(1,2**4):
            arr[i,i]=-1
        qml.QubitUnitary(arr, wires=[0,1,2,"light"])

        for i in range(3):
            qml.Hadamard(wires=i)
        #qml.Hadamard(wires=3)
    @qml.qnode(dev)
    def circuit():
        
        # QHACK #
        qml.BasisState(np.array([0,0,0,0]),wires=[0, 1, 2, "light"])
        for i in range(3):
            qml.Hadamard(wires=i)

        qml.PauliX(wires="light")       

        qml.Hadamard(wires="light")

        oracle()
        for i in range(3):
              qml.Hadamard(wires=i)

        Ufo()  
        
        qml.CNOT(wires=[0,"light"])
        qml.CNOT(wires=[1,"light"])
        qml.CNOT(wires=[2,"light"])      
        qml.ctrl(qml.Hadamard,control=[1,2,"light"])(wires=0)    
        qml.ctrl(qml.Hadamard,control=[0,2,"light"])(wires=1)          
        qml.ctrl(qml.Hadamard,control=[0,1,"light"])(wires=2)          
        qml.CNOT(wires=[0,"light"])
        qml.CNOT(wires=[1,"light"])
        qml.CNOT(wires=[2,"light"])              

        Ufo()


        # QHACK #

        return qml.sample(wires=[0,1,2])

    sample = circuit()
    sample=np.array(sample)
    res= sample[0]*1+sample[1]*2+sample[2]*4

    if res==1:
        return [0]
    elif res==3:
        return[0,1]
    elif res==2:
        return[1]
    elif res==4:
        return[2]
    elif res==5:
        return[0,2]
    elif res==6:
        return[1,2]
    elif res==7:
        return[0,1,2]


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    numbers = [int(i) for i in inputs]

    def oracle():
        for i in numbers:
            qml.CNOT(wires=[i, "light"])

    output = switch(oracle)
    print(*output, sep=",")
