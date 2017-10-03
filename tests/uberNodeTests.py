import os
import sys

thisDirPath = os.path.dirname( os.path.abspath( __file__ ) )
uberPath = os.path.join( thisDirPath, '..' )
if uberPath not in sys.path:
    sys.path.append( uberPath )
import unittest

from uberNode import UberNode


class Variable( UberNode ):
    
    def __init__( self, value, **kwargs ):
        UberNode.__init__( self, **kwargs )

        self.addOutput( 'value', value )


class Add( UberNode ):

    def __init__( self, **kwargs ):
        UberNode.__init__( self, **kwargs )

        self.addOutput( 'result' )
    
    def evaluate( self ):
        a = self.getInputValue( 'a' )
        b = self.getInputValue( 'b' )
        self.setOutputValue( 'result', a + b )


class TestStringMethods( unittest.TestCase ):

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

    def test_connect( self ):
        input1 = Variable( 1 )
        input2 = Variable( 2 )
        add = Add()
        add.inputs['a'] = input1.outputs['value']
        add.inputs['b'] = input2.outputs['value']
        add.evaluate()
        self.assertTrue( add.getOutputValue( 'result' ) == 3 )

    def test_reconnect( self ):
        input1 = Variable( 1 )
        input2 = Variable( 2 )
        input3 = Variable( 3 )
        add = Add()
        add.inputs['a'] = input1.outputs['value']
        add.inputs['b'] = input2.outputs['value']
        add.evaluate()
        oldValue = add.getOutputValue( 'result' )
        add.inputs['b'] = input3.outputs['value']
        add.evaluate()
        newValue = add.getOutputValue( 'result' )
        self.assertTrue( oldValue == 3 and newValue == 4 )

    def test_chain( self ):

        # Add 2 and 1.
        input1 = Variable( 1 )
        input2 = Variable( 2 )
        add1 = Add()
        add1.inputs['a'] = input1.outputs['value']
        add1.inputs['b'] = input2.outputs['value']
        add1.evaluate()

        # Add the result to 3.
        input3 = Variable( 3 )
        add2 = Add()
        add2.inputs['a'] = add1.outputs['result']
        add2.inputs['b'] = input3.outputs['value']
        add2.evaluate()

        self.assertTrue( add1.getOutputValue( 'result' ) == 3 and add2.getOutputValue( 'result' ) == 6 )


if __name__ == '__main__':
    unittest.main()