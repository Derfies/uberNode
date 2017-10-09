# class ValueWrapper( object ):

#     def __init__( self, node, value=None, type_=None ):
#         self.node = node
#         self.value = value
#         self.type = type_   # For type checking, which we may want to do.


class UberNode( object ):

    def __init__( self, **kwargs ):
        self.parent = kwargs.get( 'parent' )
        self.children = kwargs.get( 'children', [] )
        self.inputs = {}
        self.outputs = {}

        # HAXXOR
        self.inputConnections = {}
        self.outputConnections = {}

    def setParent( self, parent ):
        if self.parent is not None:
            self.parent.children.remove( self )
        self.parent = parent
        self.parent.children.append( self )

    # def append( self, node ):
    #     pass

    # def getInputValue( self, name ):
    #     return self.inputs[name].value

    # def setInputValue( self, name, value ):

    #     # TO DO - Type checking?
    #     self.inputs[name].value = value

    def addInput( self, name ):
        self.inputs[name] = None

    def addOutput( self, name, value=None ):
        self.outputs[name] = value#ValueWrapper( self, value )

    def getOutputValue( self, name=None ):
        if name is None:
            assert len( self.outputs ) == 1, 'Must specify an output name'
            name = self.outputs.keys()[0]
        return self.outputs[name]#.value

    def setOutputValue( self, name, value ):
        self.outputs[name] = value

    def connect( self, outputName, inputNode, inputName ):

        # Add input / output connections. Inputs can only have one connection
        # whereas outputs can have many.
        outputConnections = self.outputConnections.setdefault( outputName, [] )
        outputConnections.append( (inputNode, inputName) )
        inputNode.inputConnections[inputName] = (self, outputName)

        # Evaluate all nodes. TO DO - Make this recursive. Also needs more smarts
        # for complex graphs, I imagine. 
        dirtyNodes = []
        for outputName, connections in self.outputConnections.items():
            for connection in connections:
                node, inputName = connection
                dirtyNodes.append( node )
        for node in list( set( dirtyNodes ) ):
            node.doEvaluation()

    def evaluate( self, **inputs ):
        """Take inputs, run code, produce outputs."""
        return {}

    def doEvaluation( self ):

        inputs = {
            inputName: connection[0].getOutputValue( connection[1] )
            for inputName, connection in self.inputConnections.items()
        }

        # Only calculate if the required inputs matches the input connections.
        if set( inputs.keys() ) == set( self.inputs.keys() ):
            results = self.evaluate( **inputs )
            for k, v in results.items():
                assert k in self.outputs, 'Calculated value "' + k + '" which is not an output'
                self.setOutputValue( k, v )
 

if __name__ == '__main__':
    pass