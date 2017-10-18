class UberNode( object ):

    def __init__( self, **kwargs ):
        self.name = kwargs.get( 'name' )
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
        assert name not in self.outputs, 'Output "{}" already exists'.format( name )
        self.outputs[name] = value

    def addStaticOutput( self, name, value=None ):

        cls = type( self )

        def fget( self ):
            return getattr( self, '_' + name )

        def fset( self, value ):
            setattr( self, '_' + name, value )
            self.doEvaluation() 
        
        self.addOutput( name, value )
        setattr( cls, '_' + name, value )
        setattr( cls, name, property( fget, fset ) )

    def getInputValue( self, name=None ):

        # For convenience. If there is only one input then the name kwarg isn't
        # necessary.
        if name is None:
            assert len( self.inputs ) == 1, 'Must specify an input name'
            name = self.inputs[0]
        return self.getInputs()[name]

    def getOutputValue( self, name=None ):

        # For convenience. If there is only one output then the name kwarg isn't
        # necessary.
        if name is None:
            assert len( self.outputs ) == 1, 'Must specify an output name'
            name = self.outputs.keys()[0]
        assert name in self.outputs, 'Output "{}" does not exist'.format( name )
        return self.outputs[name]

    def connect( self, outputName, inputNode, inputName ):
        assert inputName in inputNode.inputs, 'Input "{}" does not exist'.format( inputName )
        assert outputName in self.outputs, 'Output "{}" does not exist'.format( outputName )

        # Add input / output connections. Inputs can only have one connection
        # whereas outputs can have many.
        outputConnections = self.outputConnections.setdefault( outputName, [] )
        outputConnections.append( (inputNode, inputName) )
        inputNode.inputConnections[inputName] = (self, outputName)
        self.evaluateDirtyNodes()

    def disconnect( self, outputName ):
        print self.outputConnections.setdefault[outputName]

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

    def getInputs( self ):
        return {
            inputName: connection[0].getOutputValue( connection[1] )
            for inputName, connection in self.inputConnections.items()
        }

    def doEvaluation( self ):
        inputs = self.getInputs()

        # Only calculate if the required inputs matches the input connections.
        if set( inputs.keys() ) == set( self.inputs ):
            results = self.evaluate( **inputs )
            assert hasattr( results, 'keys' ) and set( results.keys() ) == set( self.outputs.keys() ), 'Evaluate did not return expected values'
            for k, v in results.items():
                self.outputs[k] = v
                self.evaluateDirtyNodes()

    def evaluate( self, **inputs ):
        """Take inputs, run code, produce outputs."""
        return {}
 

if __name__ == '__main__':
    pass