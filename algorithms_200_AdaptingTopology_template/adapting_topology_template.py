#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml

graph = {
    0: [1],
    1: [0, 2, 3, 4],
    2: [1],
    3: [1],
    4: [1, 5, 7, 8],
    5: [4, 6],
    6: [5, 7],
    7: [4, 6],
    8: [4],
}


def n_swaps(cnot):
    """Count the minimum number of swaps needed to create the equivalent CNOT.

    Args:
        - cnot (qml.Operation): A CNOT gate that needs to be implemented on the hardware
        You can find out the wires on which an operator works by asking for the 'wires' attribute: 'cnot.wires'

    Returns:
        - (int): minimum number of swaps
    """

    # QHACK #
    s=cnot.wires[0]
    a=cnot.wires[1]
    n=9
    visited=[False]*n
    q=[]
    d=[-1]*n
    
    test=False
    q.append(s)
    visited[s]=True
    while(q):
        v=q.pop(0)
        if (v==a):
            test=True
            break
        for u in graph[v]:      
            if(not visited[u]):
                d[u]=d[v]+1
                visited[u]=1
                q.append(u)
                
                    
    
    return d[a]*2
    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    output = n_swaps(qml.CNOT(wires=[int(i) for i in inputs]))
    print(f"{output}")
