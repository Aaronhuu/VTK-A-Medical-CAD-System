'''
Created on Jun 13, 2016

@author: aaronhu
'''
import vtk


class SplineCurveInteractorStyle(vtk.vtkInteractorStyleImage):
    '''
    Handle the style of the point select and curve making.
    '''
    


    def __init__(self, params):
        '''
        Constructor
        '''
        