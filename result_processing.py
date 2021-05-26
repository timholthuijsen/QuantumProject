# -*- coding: utf-8 -*-
"""
Created on Mon May 24 14:31:48 2021

@author: luka5132
"""
import matplotlib.pyplot as plt
import numpy as np
import json


with open('quantum_gates.json', 'r') as f:
    basic_res = json.load(f)
#print(basic_res)

brkeys = list(basic_res.keys())
newdict = {}
for akey in brkeys:
    resdict = basic_res[akey]
    reskeys = list(resdict.keys())
    cordict = {}
    bitlist = []
    list0 = []
    list1 = []
    for rskey in reskeys:
        key_spl = rskey.split("_")
        if len(key_spl) > 1:
            r = resdict[rskey]
            bs = key_spl[0]
            bitlist.append(bs)
            list0.append(r['0'])
            list1.append(r['1'])
    cordict["bitlist"] = bitlist
    cordict["list0"] = list0
    cordict["list1"] = list1
    newdict[akey] = cordict
    
#print(newdict)

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

def n_correct(bl, list_0, correct_op):
    correct_list = []
    wrong_list = []
    for i,b in enumerate(bl):
        aa = int(b[0])
        bb = int(b[1])
        cor = correct_op(aa,bb)
        if cor == 0:
            correct_list.append(list_0[i])
            wrong_list.append(250 - list_0[i])
        else:
            correct_list.append(250 -list_0[i])
            wrong_list.append(list_0[i])
    return correct_list,wrong_list

nandex = newdict['NAND']
nand_bl = nandex['bitlist']
nand_l0 = nandex['list0']
print(n_correct(nand_bl, nand_l0, ournand))

def make_plot(opname, cor_func, plotname):
    opdict = newdict[opname]
    bl = opdict['bitlist']
    l0 = opdict['list0']
    l1 = opdict['list1']
    cor, wr = n_correct(bl, l0, cor_func)
    tot_cor = sum(cor)
    tot_wr = sum(wr)
    ind = np.arange(4)
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    yes = ax.bar(ind, cor, width = 0.25)
    no = ax.bar(ind + 0.25, wr, width = 0.25)
    plt.title(plotname)
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels(bl)
    ax.legend( (yes[0],no[0]), ('correct','wrong') )
    
    return tot_cor, tot_wr

def plot_not():
    opdict = newdict['NOT']
    bl = opdict['bitlist']
    l0 = opdict['list0']
    l1 = opdict['list1']
    cor = [l1[0], l0[1]]
    wr = [l0[0], l1[1]]
    tot_cor = sum(cor)
    tot_wr = sum(wr)
    ind = np.arange(2)
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    yes = ax.bar(ind, cor, width = 0.25)
    no = ax.bar(ind + 0.25, wr, width = 0.25)
    plt.title('NOT-gate')
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels(bl)
    ax.legend( (yes[0],no[0]), ('correct','wrong') )
    
    return tot_cor, tot_wr