import collections


class BasePuts( collections.MutableMapping ):

    def __init__( self, node, keys ):
        self._node = node
        self._keys = keys
        self._data = {}
        self._connections = {}

    def __len__( self ):
        return len( self._data )

    def __iter__( self ):
        return iter( self._data )

    def __getitem__( self, key ):
        raise NotImplementedError

    def __setitem__( self, key, value ):
        self._data[key] = value

    def __delitem__( self, key ):
        del self._data[key]


class Inputs( BasePuts ):

    def __getitem__( self, key ):
        if key in self._connections:
            output, outputName = self._connections[key]
            return output[outputName]
        else:
            return self._data[key]

    def __setitem__( self, key, value ):
        super( Inputs, self ).__setitem__( key, value )

        self._node.onEvaluate()

    def connect( self, inputName, output, outputName, connectInverse=True ):

        # Add input / output connections. Inputs can only have one connection
        # whereas outputs can have many.
        self._connections[inputName] = (output, outputName)
        if connectInverse:
            output.connect( outputName, self, inputName, connectInverse=False )
        self._node.onEvaluate()

    def allConnected( self ):
        return set( self._keys ) & set( self._data.keys() ) == set( self._keys )


class Outputs( BasePuts ):

    def __getitem__( self, key ):
        if key not in self._keys:
            raise KeyError( 'output \'' + key + '\' does not exist' )
        elif key in self._keys and key not in self._data:
            raise KeyError( 'node has not been evaluated' )
        return self._data[key]

    def __setitem__( self, key, value ):
        if key not in self._keys:
            raise KeyError( 'output \'' + key + '\' does not exist' )
        super( Outputs, self ).__setitem__( key, value )

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

        self.inputs = Inputs( self, kwargs.get( 'inputs', [] ) )
        self.outputs = Outputs( self, kwargs.get( 'outputs', [] ) )

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
        if self.inputs.allConnected():
            self.evaluate()
            self.evaluateDownstreamNodes()

    def evaluate( self, **inputs ):
        """Take inputs, run code, produce outputs."""
        pass
 

if __name__ == '__main__':
    pass