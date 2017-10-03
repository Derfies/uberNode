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

    def evaluate( self ):
        """Take inputs, run code, produce outputs."""
        pass
 

if __name__ == '__main__':
    pass