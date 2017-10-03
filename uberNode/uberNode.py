class ValueWrapper( object ):

    def __init__( self, value=None, type_=None ):
        self.value = value
        self.type = type_   # For type checking, which we may want to do.


class UberNode( object ):

    def __init__( self, **kwargs ):
        self.parent = kwargs.get( 'parent' )
        self.children = kwargs.get( 'children', [] )
        self.inputs = {}
        self.outputs = {}

    def setParent( self, parent ):
        if self.parent is not None:
            self.parent.children.remove( self )
        self.parent = parent
        self.parent.children.append( self )

    def append( self, node ):
        pass

    def getInputValue( self, name ):
        return self.inputs[name].value

    def setInputValue( self, name, value ):

        # TO DO - Type checking?
        self.inputs[name].value = value

    def addOutput( self, name, value=None ):
        self.outputs[name] = ValueWrapper( value )

    def getOutputValue( self, name ):
        return self.outputs[name].value

    def setOutputValue( self, name, value ):
        self.outputs[name].value = value

    #def connect( self, inputName, outputName ):
    #    self.inputs[inputName] = input1.outputs['value']

    def evaluate( self ):
        """Take inputs, run code, produce outputs."""
        pass
 

if __name__ == '__main__':
    pass