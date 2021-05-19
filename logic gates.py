# -*- coding: utf-8 -*-
"""
Created on Tue May 18 18:19:42 2021

@author: user
"""
#not / and / or /  implies / nand gates


import cirq


def and_q(cq1, cq2, tq):
    circuit = cirq.Circuit()

    # +------------------------+
    # |Type your solution below|
    # +------------------------+
    circuit.append(cirq.CCX(cq1,cq2,tq))
    # +------------------------+
    # |Type your solution above|
    # +------------------------+

    return circuit

def nand_q(cq1, cq2, tq):
    circuit = cirq.Circuit()

    # +------------------------+
    # |Type your solution below|
    # +------------------------+
    circuit.append(cirq.CCX(cq1,cq2,tq))
    
    circuit.append(cirq.X(tq))
    # +------------------------+
    # |Type your solution above|
    # +------------------------+

    return circuit

#works on 1 qubit 
def not_q(tq):
    circuit = cirq.Circuit()

    # +------------------------+
    # |Type your solution below|
    # +------------------------+    
    circuit.append(cirq.X(tq))
    # +------------------------+
    # |Type your solution above|
    # +------------------------+

    return circuit

def implies_q(cq1,cq2,tq):
    circuit = cirq.Circuit()

    # +------------------------+
    # |Type your solution below|
    # +------------------------+    
    circuit.append(cirq.X(cq2))
    circuit.append(cirq.CCX(cq1,cq2,tq))
    circuit.append(cirq.X(tq))
    # +------------------------+
    # |Type your solution above|
    # +------------------------+

    return circuit


#the tests are for "and" now. I tested all the functions with function below by adjusting function name
#they seem to work. 
if __name__ == "__main__":
    cq1 = cirq.GridQubit(1, 0)
    cq2 = cirq.GridQubit(1, 1)
    tq = cirq.GridQubit(0, 2)
    circuit = cirq.Circuit()
    and_q2_circuit = and_q(cq1, cq2, tq)
    #circuit.append([cirq.X(cq2)])
    #circuit.append([cirq.X(cq1), cirq.X(cq2)])
    circuit.append(and_q2_circuit.all_operations())
    circuit.append(
        [
            cirq.measure(cq1, key="x1"),
            cirq.measure(cq2, key="x2"),
            cirq.measure(tq, key="x3"),
        ]
    )
    res = cirq.Simulator().run(circuit, repetitions=20)
    print_circuit = lambda circuit: "  " + (
        str(circuit).replace("\n", "\n  ")
        if len(circuit) > 0
        else "<<This circuit contains no gates.>>"
    )
    print("We are testing your circuit on the input x1 = 1, x2 = 1.")
    print("Your circuit looks like this:")
    print()
    print(print_circuit(and_q2_circuit))
    print()
    print("The complete circuit looks like this:")
    print()
    print(print_circuit(circuit))
    print()
    
    print(
        "If you implemented the or2 circuit correctly, we should obtain the following measurement outcomes:"
    )
    print()
    print("  x1={}".format("1" * 20))
    print("  x2={}".format("1" * 20))
    print("  x3={}".format("1" * 20))
    print()

    print("The actual outcome is:")
    print()
    print(
        "  "
        + (
            str(res).replace("\n", "\n  ")
            if len(res.measurements) > 0
            else "<<There were no measurements.>>"
        )
    )
    print()
