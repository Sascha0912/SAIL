from pygem import StlHandler

def loadBaseWheelcase(expressionFunction, dof):
    stl_handler = StlHandler()

    class Base: # what do we need to load for the wheelcase domain?
        def __init__(self):
            self.coordinates = stl_handler.parse('domain/wheelcase/ffd/wheelcase.stl') # coordinates of mesh

    return Base()
