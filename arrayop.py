#!/usr/bin/env python3

import numpy as np
from uncertainties import unumpy as unp
from uncertainties.unumpy import nominal_values as nvs, std_devs as sds

def arrayop(arr1, arr1err, arr2, arr2err, op):

    uarr1 = unp.uarray(arr1, arr1err)
    uarr2 = unp.uarray(arr2, arr2err)

    if op == '+': uarr = uarr1 + uarr2
    elif op == 'ave': uarr = 0.5*(uarr1 + uarr2)
    elif op == '-': uarr = uarr1 - uarr2
    elif op == '*': uarr = uarr1 * uarr2
    elif op == '/': uarr = uarr1 / uarr2
    elif op == '+^2': uarr = np.sqrt(uarr1**2 + uarr2**2)
    elif op == '-^2': uarr = np.sqrt(uarr1**2 - uarr2**2)
    elif op == '/^2': uarr = uarr1 / uarr2**2
    else: ValueError('Operator not recognized')

    return nvs(uarr), sds(uarr)
