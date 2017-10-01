class UberNode( object ):

    def __init__( self ):#, id_, title ):
        #self.id = id_
        #self.title = title

        self.parent = None
        self.children = []
        self.inputs = {}
        self.outputs = {}

    def setParent( self, parent ):
        if self.parent is not None:
            self.parent.children.remove( self )
        self.parent = parent
        self.parent.children.append( self )

    def append( self, node ):
        pass

    def eval( self ):
        """Take inputs, run code, produce outputs."""
        pass
 

if __name__ == '__main__':


    class Input1( UberNode ):
        
        def __init__( self, *args, **kwargs ):
            UberNode.__init__( self, *args, **kwargs )

            self.outputs['value'] = 7


    class Input2( UberNode ):
        
        def __init__( self, *args, **kwargs ):
            UberNode.__init__( self, *args, **kwargs )

            self.outputs['value'] = 5


    class Constant( UberNode ):
        
        def __init__( self, *args, **kwargs ):
            UberNode.__init__( self, *args, **kwargs )

            self.outputs['value'] = 5


    class Add( UberNode ):
        
        def eval( self ):
            return self.inputs['input1'] + self.inputs['input2']


    input1 = Input1()
    input2 = Input2()
    add = Add()
    add.inputs['input1'] = input1.outputs['value']
    add.inputs['input2'] = input2.outputs['value']

    print add.eval()
    print 'done'

    # Conundrum: where to define input / output keys? In the class definition?
    # As user: want to edit value only
    # As dev: probably want to minimise the number of classes needed to create complex graphs