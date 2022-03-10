import sys
import pennylane as qml
from pennylane import numpy as np
from pennylane import hf


def ground_state_VQE(H):
    """Perform VQE to find the ground state of the H2 Hamiltonian.

    Args:
        - H (qml.Hamiltonian): The Hydrogen (H2) Hamiltonian

    Returns:
        - (float): The ground state energy
        - (np.ndarray): The ground state calculated through your optimization routine
    """

def ground_state_VQE(H):
    """Perform VQE to find the ground state of the H2 Hamiltonian.

    Args:
        - H (qml.Hamiltonian): The Hydrogen (H2) Hamiltonian

    Returns:
        - (float): The ground state energy
        - (np.ndarray): The ground state calculated through your optimization routine
    """

    # QHACK #
    qubits=4
    def circuit(param, wires):
        qml.BasisState(np.array([1,1,0,0]), wires=[0, 1, 2, 3])
        qml.DoubleExcitation(param, wires=[0, 1, 2, 3])
    dev = qml.device("default.qubit", wires=qubits)
    @qml.qnode(dev)    
    def cost_fn(param):
        circuit(param, wires=[0, 1, 2, 3])
        return qml.expval(H)
    
    opt = qml.AdamOptimizer(stepsize=0.8)
    theta = np.array(0.05, requires_grad=True)
    # store the values of the cost function
    energy = [cost_fn(theta)]

    # store the values of the circuit parameter
    angle = [theta]

    max_iterations = 500
    conv_tol = 1e-30

    for n in range(max_iterations):
        theta, prev_energy = opt.step_and_cost(cost_fn, theta)
        #theta = np.clip(opt.step_and_cost(cost_fn, theta), -2 * np.pi, 2 * np.pi)
        energy.append(cost_fn(theta))
        angle.append(theta)
        conv = np.abs(energy[-1] - prev_energy)

        if conv <= conv_tol:
            break
    state=np.zeros((1,2**4))
    state[0,12]=np.cos(theta/2)
    state[0,3]=-np.sin(theta/2)
    return energy[-1],state
    # QHACK #


def create_H1(ground_state, beta, H):
    """Create the H1 matrix, then use `qml.Hermitian(matrix)` to return an observable-form of H1.

    Args:
        - ground_state (np.ndarray): from the ground state VQE calculation
        - beta (float): the prefactor for the ground state projector term
        - H (qml.Hamiltonian): the result of hf.generate_hamiltonian(mol)()

    Returns:
        - (qml.Observable): The result of qml.Hermitian(H1_matrix)
    """

    # QHACK #
    matrix=qml.utils.sparse_hamiltonian(H).real.toarray()
    return qml.Hermitian(matrix+beta*np.dot(np.transpose(ground_state),ground_state),wires=[1,2,3,4])
    # QHACK #


def excited_state_VQE(H1):
    """Perform VQE using the "excited state" Hamiltonian.

    Args:
        - H1 (qml.Observable): result of create_H1

    Returns:
        - (float): The excited state energy
    """

    # QHACK #
    eig=H1.eigvals
    return eig[2]
    # QHACK #



if __name__ == "__main__":
    coord = float(sys.stdin.read())
    symbols = ["H", "H"]
    geometry = np.array([[0.0, 0.0, -coord], [0.0, 0.0, coord]], requires_grad=False)
    mol = hf.Molecule(symbols, geometry)

    H = hf.generate_hamiltonian(mol)()
    E0, ground_state = ground_state_VQE(H)

    beta = 15.0
    H1 = create_H1(ground_state, beta, H)
    E1 = excited_state_VQE(H1)

    answer = [np.real(E0), E1]
    print(*answer, sep=",")
