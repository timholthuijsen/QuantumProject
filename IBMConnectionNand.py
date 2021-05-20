import numpy as np
from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
from qiskit import *
from qiskit import IBMQ
from qiskit_gates import NAND
import json

IBMQ.load_account()
IBMQ.providers()
provider = IBMQ.get_provider('ibm-q')

from qiskit.providers.ibmq import least_busy
def lb():
    return least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 2 and 
                                        not x.configuration().simulator and x.status().operational==True))

backend = lb()
print("Using: {}".format(backend))

def AND(inp1, inp2, backend, layout, n_times = 100):
    
    qc = QuantumCircuit(3, 1) 
    qc.reset(range(3))
    
    if inp1=='1':
        qc.x(0)
    if inp2=='1':
        qc.x(1)
        
    qc.barrier()
    qc.ccx(0, 1, 2) 
    qc.barrier()
    qc.measure(2, 0) 
  
    qc_trans = transpile(qc, backend, initial_layout=layout, optimization_level=3)
    job = execute(qc_trans, backend, shots= n_times)
    print(job.job_id())
    job_monitor(job)
    
    output = job.result().get_counts()
    
    return qc_trans, output

def NOT(inp, backend, layout, n_times = 100):
    
    qc = QuantumCircuit(1, 1) # A quantum circuit with a single qubit and a single classical bit
    qc.reset(0)
    
    if inp=='1':
        qc.x(0)
    
    qc.barrier()
    # Now we've encoded the input, we can do a NOT on it using x
    qc.x(0)
    #barrier between gate operation and measurement
    qc.barrier()
    qc.measure(0,0)
    
    qc_trans = transpile(qc, backend, initial_layout=layout, optimization_level=3)
    job = execute(qc_trans, backend, shots= n_times)
    print(job.job_id())
    job_monitor(job)
    
    output = job.result().get_counts()
    
    return qc_trans, output

def XOR(inp1, inp2, backend, layout, n_times = 100):
    
    qc = QuantumCircuit(3, 1) 
    qc.reset(range(3))
    
    if inp1=='1':
        qc.x(0)
    if inp2=='1':
        qc.x(0)
    
    # barrier between input state and gate operation 
    qc.barrier()
    # this is where your program for quantum XOR gate goes
    qc.cx(2,0)
    qc.cx(2,1)
    # barrier between input state and gate operation 
    qc.barrier()

    qc.measure(0,0) # output from qubit 1 is measured
    qc_trans = transpile(qc, backend, initial_layout=layout, optimization_level=3)
    job = execute(qc_trans, backend, shots= n_times)
    print(job.job_id())
    job_monitor(job)
    
    output = job.result().get_counts()
    
    return qc_trans, output


def NAND(inp1, inp2, backend, layout, n_times = 100):
    
    qc = QuantumCircuit(3, 1) 
    qc.reset(range(3))
    
    if inp1=='1':
        qc.x(0)
    if inp2=='1':
        qc.x(1)
    
    qc.barrier()
    
    qc.ccx(0,1,2)
    qc.x(2)
    
    qc.barrier()
    qc.measure(2, 0) # output from qubit 2 is measured 
  
    qc_trans = transpile(qc, backend, initial_layout=layout, optimization_level=3)
    job = execute(qc_trans, backend, shots= n_times)
    print(job.job_id())
    job_monitor(job)
    
    output = job.result().get_counts()
    
    return qc_trans, output


def OR(inp1, inp2, backend, layout, n_times = 100):
    
    qc = QuantumCircuit(3, 1) 
    qc.reset(range(3))
    
    if inp1=='1':
        qc.x(0)
    if inp2=='1':
        qc.x(1)
    
    qc.barrier()
    
    for q in range(3):
        qc.x(q)
    qc.ccx(0,1,2)
    for q in range(2):
        qc.x(q)

    qc.barrier()
    qc.measure(2, 0) # output from qubit 2 is measured
  
    qc_trans = transpile(qc, backend, initial_layout=layout, optimization_level=3)
    job = execute(qc_trans, backend, shots= n_times)
    print(job.job_id())
    job_monitor(job)
    
    output = job.result().get_counts()
    
    return qc_trans, output

def IMPLIES(inp1, inp2, backend, layout, n_times = 100):
    
    qc = QuantumCircuit(3, 1) 
    qc.reset(range(3))
    
    if inp1=='1':
        qc.x(0)
    if inp2=='1':
        qc.x(1)
    
    qc.barrier()
    qc.x(1)
    qc.ccx(0,1,2)
    qc.x(2)
    
    qc.barrier()
    qc.measure(2, 0) # output from qubit 2 is measured
  
    qc_trans = transpile(qc, backend, initial_layout=layout, optimization_level=3)
    job = execute(qc_trans, backend, shots= n_times)
    print(job.job_id())
    job_monitor(job)
    
    output = job.result().get_counts()
    
    return qc_trans, output



def ournot(a):
    return not a
def ourxor(a,b):
    return a ^ b
def ourand(a,b):
    return a and b
def ournand(a,b):
    return not(a and b)
def ourimplies(a,b):
    return not a or b
def ouror(a,b):
    return a or b


def run_for_two_inputs(f = AND, n_tries = 100, func_ver = ourand):
    output1_all = []
    qc_trans1_all = []
    prob1_all = {}
    layout1 = [0,1,2]
    
    worst = 1
    best = 0
    for input1 in ['0','1']:
        for input2 in ['0','1']:
            tot_inp = input1 + input2
            qc_trans1, output1 = f(input1, input2, backend, layout1, n_tries)
            
            output1_all.append(output1)
            qc_trans1_all.append(qc_trans1)
            
           
            prob1_all[tot_inp + "_output"] = output1
            try:
                int1 = int(input1)
                int2 = int(input2)
                prob = output1[str(int(func_ver(int1,int2)))]/ n_tries
                prob1_all[tot_inp] = prob
            except:
                print("error with calculating probaility")
            
            print('\nProbability of correct answer for inputs',input1,input2)
            print( '{:.2f}'.format(prob) )
            print('---------------------------------')
            
            worst = min(worst,prob)
            best = max(best, prob)
            
    print('')
    print('\nThe highest of these probabilities was {:.2f}'.format(best))
    print('The lowest of these probabilities was {:.2f}'.format(worst))
    
    return(prob1_all)

def run_for_NOT(n_tries = 100):
    output1_all = []
    qc_trans1_all = []
    prob1_all = {}
    layout1 = [0]
    
    worst = 1
    best = 0
    for input1 in ['0','1']:
            qc_trans1, output1 = NOT(input1, backend, layout1, n_tries)
            
            output1_all.append(output1)
            qc_trans1_all.append(qc_trans1)
            try:
                prob = output1[str(int( not input1=='1'))]/ n_tries
                prob1_all[input1] = prob
            except:
                pass
            prob1_all[input1 + "_output"] = output1
            
            print('\nProbability of correct answer for inputs',input1)
            print( '{:.2f}'.format(prob) )
            print('---------------------------------')
            
            worst = min(worst,prob)
            best = max(best, prob)
            
    print('')
    print('\nThe highest of these probabilities was {:.2f}'.format(best))
    print('The lowest of these probabilities was {:.2f}'.format(worst))
    
    return(prob1_all)


function_list = [NOT,XOR,AND,NAND,IMPLIES,OR]
function_names = ["NOT","XOR","AND","NAND","IMPLIES","OR"]
function_verification = [ournot, ourxor, ourand, ournand, ourimplies,ouror]

def run_all(n_tries = 250):
    outputdict = {}
    for i,f in enumerate(function_list):
        fname = function_names[i]
        func_ver = function_verification[i]
        print("Starting with {} function".format(fname))
        if fname == "NOT":
            p_dict = run_for_NOT(n_tries)
        else:
            p_dict = run_for_two_inputs(f, n_tries, func_ver)
        outputdict[fname] = p_dict
    return outputdict
    
def run_and_save_json():    
    outdict = run_all()
    with open("quantum_gates.json", "w") as f:
        json.dump(outdict, f)
        
        
def fix_and():
    outdict = json.load("quantum_gates.json")
    xor_dict = run_for_two_inputs(AND, 250, ouror)
    newdict = outdict['XOR'] = xor_dict
    with open("quantum_gates2.json", "w") as f:
        json.dump(outdict, f)


if False:
    #Connect to IBM Quantum cloud computer
    token = '0d68f7931a9478843c23ed26be08465d50864f50035952b49b5e46d2764120b5e04c19c93563ecd8a6d9b0032c553d00b13be1a326c557ed0129f936d448aa62'
    #Note: Token is Tim's account specific, and subject to change
    IBMQ.save_account(token)
    provider = IBMQ.load_account()
    backend = provider.get_backend('ibmq_16_melbourne')
    
    #Put the quantum circuit here
    circuit, output = NAND(1,1)
    
    
    
    #Execute circuit on IBM quantum computer
    job = execute(circuit, backend, shots=1000)
    
    
    #Plot probability histogram
    result = job.result()
    counts = result.get_counts(circuit)
    print("\nTotal count for 00 and 11 are: {}\n".format(counts))
    
    plot_histogram(counts).savefig("IBMNandTrial.png")
    
    circuit.draw()