class Inputs( object ):

    def __init__( self, node, inputs ):
        self._node = node
        self._inputs = inputs
        self._connections = {}

    def __getitem__( self, *args ):
        key = args[0]
        if key in self._connections:
            output, outputName = self._connections[key]
            return output[outputName]
        else:
            return self._inputs[key]

    def __setitem__( self, *args ):
        self._inputs.update( {args[0]: args[1]} )
        self._node.onEvaluate()

    def connect( self, inputName, output, outputName, connectInverse=True ):

        # Add input / output connections. Inputs can only have one connection
        # whereas outputs can have many.
        self._connections[inputName] = (output, outputName)
        if connectInverse:
            output.connect( outputName, self, inputName, connectInverse=False )
        self._node.onEvaluate()


class Outputs( object ):

    def __init__( self, node, outputs ):
        self._node = node
        self._outputs = outputs
        self._connections = {}

    def __getitem__( self, *args ):
        return self._outputs[args[0]]

    def __setitem__( self, *args ):
        self._outputs.update( {args[0]: args[1]} )

    def connect( self, outputName, input_, inputName, connectInverse=True ):

        # Add input / output connections. Inputs can only have one connection
        # whereas outputs can have many.
        conns = self._connections.setdefault( outputName, [] )
        conns.append( (input_, inputName) )
        if connectInverse:
            input_.connect( inputName, self, outputName, connectInverse=False )


class UberNode( object ):

    def __init__( self, **kwargs ):
        self.name = kwargs.get( 'name' )
        self.parent = kwargs.get( 'parent' )
        self.children = kwargs.get( 'children', [] )

        self.inputs = Inputs( self, kwargs.get( 'inputs', {} ) )
        self.outputs = Outputs( self, kwargs.get( 'outputs', {} ) )

        # Big question about design here. How do we handle if evaluate is all
        self.onEvaluate()

    def setParent( self, parent ):
        if self.parent is not None:
            self.parent.children.remove( self )
        self.parent = parent
        self.parent.children.append( self )

    def append( self, node ):
        node.setParent( self )

    def evaluateDownstreamNodes( self ):

        # Evaluate all nodes. TO DO - Make this recursive. Also needs more smarts
        # for complex graphs, I imagine. 
        dirtyNodes = []
        for outputName, conns in self.outputs._connections.items():
            for conn in conns:
                input_, inputName = conn
                dirtyNodes.append( input_._node )
        for node in list( set( dirtyNodes ) ):
            node.onEvaluate()

    def onEvaluate( self ):
        self.evaluate()
        self.evaluateDownstreamNodes()

    def evaluate( self, **inputs ):
        """Take inputs, run code, produce outputs."""
        return {}
 

if __name__ == '__main__':
    pass