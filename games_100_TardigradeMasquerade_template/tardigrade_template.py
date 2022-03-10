import sys
import pennylane as qml
from pennylane import numpy as np


def second_renyi_entropy(rho):
    """Computes the second Renyi entropy of a given density matrix."""
    # DO NOT MODIFY anything in this code block
    rho_diag_2 = np.diagonal(rho) ** 2.0
    return -np.real(np.log(np.sum(rho_diag_2)))


def compute_entanglement(theta):
    """Computes the second Renyi entropy of circuits with and without a tardigrade present.

    Args:
        - theta (float): the angle that defines the state psi_ABT

    Returns:
        - (float): The entanglement entropy of qubit B with no tardigrade
        initially present
        - (float): The entanglement entropy of qubit B where the tardigrade
        was initially present
    """

    dev1 = qml.device("default.qubit", wires=3)

    # QHACK #
    @qml.qnode(dev1)
    def with_tardigrade():
        qml.Hadamard(wires=0)
        qml.PauliX(wires=1)
        qml.RY(theta,wires=2)

        qml.CNOT(wires=[2,1])
        qml.Toffoli(wires=[0,1,2])

        qml.CNOT(wires=[0,1])
        qml.CNOT(wires=[0,2])

        qml.CRY(-theta,wires=[0,1])
        
        return qml.density_matrix([1])
        
    dev2 = qml.device("default.qubit", wires=2)
    
    @qml.qnode(dev2)
    def no_tartigrade():
        qml.PauliX(wires=1)
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0,1])
        return qml.density_matrix([1])
    # QHACK #
    
    abt=second_renyi_entropy(with_tardigrade())
    ab=second_renyi_entropy(no_tartigrade())
    
    return ab,abt


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    theta = np.array(sys.stdin.read(), dtype=float)

    S2_without_tardigrade, S2_with_tardigrade = compute_entanglement(theta)
    print(*[S2_without_tardigrade, S2_with_tardigrade], sep=",")
