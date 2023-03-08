# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 11:35:25 2021

@author: G-GRE-GRE050402
"""

import numpy as np
import qcodes as qc

class Correction_matrix():
    """
    This is a matrix used for compensated parameters, is initialized to Identity upon creation.
    Modified using set_coefficient
    
    __call__ returns the matrix
    """
    def __init__(self, dimension):
        self._dimension = dimension
        self._matrix = np.identity(dimension)
        
    def __call__(self):
        return self._matrix
    
    def set_coefficient(self, row, column, value):
        self._matrix[row, column] = value
        
    def get_inverse_matrix(self):
        return np.linalg.inv(self._matrix)

    def reinitialize(self):
        self._matrix = np.identity(self._dimension)

class Generalized_compensated_parameter(qc.Parameter):
    """
    mutiple compensated parameters. Typically used for gates compensations
    inputs: 

        all the other virtual parameters
        the corresponding target parameters
        the correction matrix object
    
    example:
        m = Correction_matrix(2)
        
        G1v = Generalized_compensated_parameter('G1v') // this does NOTHING but creating the parameters
        G2v = Generalized_compensated_parameter('G2v') //

        G1v.set_corrections([G1v, G2v], [G1,G2], m) // this gives the corrections, target gates and matrix
        G2v.set_corrections([G1v, G2v], [G1,G2], m) //
        
        m.set_coefficient(0,1,-0.1) // set off coefficient of the matrix
        
        IMPORTANT:
        
        if you modify the matrix coefficients, you need to update the current_values 
        by calling G1v.recalculate_current_values() (any G2v also works, but calling only one is necessary)
        
        if you modify the target gates directly e.g. G1 or G2, you need to update the current_values 
        by calling G1v.recalculate_current_values() (any G2v also works, but calling only one is necessary)
        
        
    """
    
    
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        
    def set_corrections(self, all_corrected_parameters, target_parameters, matrix, offsets = None):
        """
        example :
        all_corrected_parameters = [G1v, G2v]
        target_parameters = [G1, G2]
        matrix = matrix_compensation object
        offset = [0.15, 0.16], this is in the target_parameters space
        """
        self._all_corrected_parameters = all_corrected_parameters

        self._corrected_parameter_index = all_corrected_parameters.index(self)

        self._target_parameters = target_parameters
        self._matrix = matrix      

        self._offsets = np.array(offsets if offsets != None else [0.]*len(self._all_corrected_parameters))

        self.recalculate_current_values()
        #self._current_value = self._target_parameters[self._corrected_parameter_index]() / self._matrix()[self._corrected_parameter_index, self._corrected_parameter_index]
        
    def get_raw(self):
        return self._current_value
        
    def set_raw(self, value):
        self._current_value = value
        
        current_values = [g() for g in self._all_corrected_parameters]
    
        current_values[self._corrected_parameter_index] = value
        corrected_values = np.dot(current_values,self._matrix())
        corrected_values += self._offsets
        for value, param in zip(corrected_values, self._target_parameters):
            param(value)
    
    def recalculate_current_values(self):
        """
        this needs to be called after updating the correction matrix 
        or
        after modifing the target gates
        """
        _target_parameters = np.array([g() for g in self._target_parameters])
        _target_parameters -= self.offsets

        current_values = np.dot(self._matrix.get_inverse_matrix(), _target_parameters)
        for v, g in zip(current_values, self._all_corrected_parameters):
            g._current_value =  v