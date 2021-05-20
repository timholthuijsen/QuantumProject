import numpy as np
from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
from qiskit import IBMQ



#Connect to IBM Quantum cloud computer
token = 'fa02ce6530d2d39489dae6cff3b599d2c239d0b5267a6a2f3e1c2218e0a62214c849571b04ded1e1071a868e404bc93311fd5f0481f421beeb7689d497c52677'
#Note: Token is Tim's account specific, and subject to change
IBMQ.save_account(token)
provider = IBMQ.load_account()
backend = provider.get_backend('ibmq_qasm_simulator')

"""
This is where to write the quantum circuit.
Note that the function will not work without a functioning circuit.
circuit needs to be defined in the format:
    circuit = makeyourcircuit
Our Qiskit_gate functions return the circuit and the output, so use format:
    circuit, output = NAND(1,1)
And:
    from qiskit_gates import NAND
"""



#Execute circuit on IBM quantum computer
job = execute(circuit, backend, shots=1000)


#Plot probability histogram
result = job.result()
counts = result.get_counts(circuit)
print("\nTotal count for 00 and 11 are: {}\n".format(counts))

plot_histogram(counts).savefig("IBMNandTrial.png")

circuit.draw()