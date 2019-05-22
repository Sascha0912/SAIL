from pygem import StlHandler

def loadBaseCube(expressionFunction, dof):
    stl_handler = StlHandler()

    class Base: # what do we need to load for the cube domain?
        def __init__(self):
            self.coordinates = stl_handler.parse('domain/cube/ffd/20mm_cube_hr.stl') # coordinates of mesh

    return Base()