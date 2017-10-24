import os
import sys
import unittest

thisDirPath = os.path.dirname( os.path.abspath( __file__ ) )
uberPath = os.path.join( thisDirPath, '..' )
if uberPath not in sys.path:
    sys.path.append( uberPath )
from uberNode import UberNode


class Add( UberNode ):

    def __init__( self ):
        UberNode.__init__( self, inputs={'a': 0, 'b': 0} )

    def evaluate( self ):
        self.outputs['result'] = self.inputs['a'] + self.inputs['b']


class Variable( UberNode ):

    def __init__( self ):
        UberNode.__init__( self, inputs={'value': None}, outputs={'result': None} )

    def evaluate( self ):
        self.outputs['result'] = self.inputs['value']


class UberNodeTests( unittest.TestCase ):

    def test_parent( self ):
        parent = UberNode()
        child = UberNode()
        child.setParent( parent )
        self.assertTrue( child.parent == parent and child in parent.children )

    def test_reparent( self ):
        parent1 = UberNode()
        parent2 = UberNode()
        child = UberNode()
        child.setParent( parent1 )
        child.setParent( parent2 )
        self.assertTrue( child.parent == parent2 and child in parent2.children and child.parent != parent1 and child not in parent1.children )

    def test_simple( self ):
        add = Add()
        self.assertTrue( add.outputs['result'] == 0 )

    def test_changeInputs( self ):
        add = Add()
        add.inputs['a'] = 1
        add.inputs['b'] = 2
        self.assertTrue( add.outputs['result'] == 3 )

    def test_connectInput( self ):
        add = Add()
        add.inputs['a'] = 1
        var = Variable()
        var.inputs['value'] = 2
        add.inputs.connect( 'b', var.outputs, 'result' )
        self.assertTrue( add.outputs['result'] == 3 )

    def test_connectOutput( self ):
        add = Add()
        add.inputs['a'] = 1
        var = Variable()
        var.inputs['value'] = 2
        var.outputs.connect( 'result', add.inputs, 'b' )
        self.assertTrue( add.outputs['result'] == 3 )

    def test_changeInput( self ):
        add = Add()
        add.inputs['a'] = 1
        var = Variable()
        var.inputs['value'] = 2
        add.inputs.connect( 'b', var.outputs, 'result' )
        var.inputs['value'] = 3
        self.assertTrue( add.outputs['result'] == 4 )

    def test_chain( self ):
        vars_ = []
        for i in range( 3 ):
            var = Variable()
            if i > 0:
                prevVar = vars_[len( vars_ ) - 1]
                var.inputs.connect( 'value', prevVar.outputs, 'result' )
            vars_.append( var )
        vars_[0].inputs['value'] = 1
        self.assertTrue( vars_[len( vars_ ) - 1].outputs['result'] == 1 )

    def test_disconnect( self ):
        pass



if __name__ == '__main__':
    unittest.main()