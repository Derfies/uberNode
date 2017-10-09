class UberNode( object ):

    def __init__( self, **kwargs ):
        self.parent = kwargs.get( 'parent' )
        self.children = kwargs.get( 'children', [] )

        self.inputs = []
        self.outputs = {}
        self.inputConnections = {}
        self.outputConnections = {}

    def setParent( self, parent ):
        if self.parent is not None:
            self.parent.children.remove( self )
        self.parent = parent
        self.parent.children.append( self )

    def append( self, node ):
        node.setParent( self )

    def addInput( self, name ):
        assert name not in self.inputs, 'Input "{}" already exists'.format( name )
        self.inputs.append( name )

    def addOutput( self, name, value=None ):
        self.outputs[name] = value

    def getOutputValue( self, name=None ):
        if name is None:
            assert len( self.outputs ) == 1, 'Must specify an output name'
            name = self.outputs.keys()[0]
        return self.outputs[name]

    def setOutputValue( self, name, value ):
        self.outputs[name] = value
        self.evaluateDirtyNodes()

    def connect( self, outputName, inputNode, inputName ):

        # Add input / output connections. Inputs can only have one connection
        # whereas outputs can have many.
        outputConnections = self.outputConnections.setdefault( outputName, [] )
        outputConnections.append( (inputNode, inputName) )
        inputNode.inputConnections[inputName] = (self, outputName)
        self.evaluateDirtyNodes()

    def evaluateDirtyNodes( self ):

        # Evaluate all nodes. TO DO - Make this recursive. Also needs more smarts
        # for complex graphs, I imagine. 
        dirtyNodes = []
        for outputName, connections in self.outputConnections.items():
            for connection in connections:
                node, inputName = connection
                dirtyNodes.append( node )
        for node in list( set( dirtyNodes ) ):
            node.doEvaluation()

    def doEvaluation( self ):

        inputs = {
            inputName: connection[0].getOutputValue( connection[1] )
            for inputName, connection in self.inputConnections.items()
        }

        # Only calculate if the required inputs matches the input connections.
        if set( inputs.keys() ) == set( self.inputs ):
            results = self.evaluate( **inputs )
            for k, v in results.items():
                assert k in self.outputs, 'Calculated value "' + k + '" which is not an output'
                self.setOutputValue( k, v )

    def evaluate( self, **inputs ):
        """Take inputs, run code, produce outputs."""
        return {}
 

if __name__ == '__main__':
    pass